"""
AFAC2026 赛题三：优化版训练
解决预测过于集中的问题
"""

import torch
import torch.nn.functional as F
import numpy as np
import pandas as pd
import os
import sys
import zipfile
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.afac2026_data_loader import load_afac2026_real_data, create_train_val_split, normalize_graph_features
from src.entity_layer.models import GCN, GATv2, MLP

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {DEVICE}", flush=True)

def train_classification():
    """产品分类任务 - 优化版"""
    print("\n=== 产品分类任务 A1 ===", flush=True)
    
    # 加载数据
    data = load_afac2026_real_data('./data/A分类/A1.npz')
    data = normalize_graph_features(data)
    data = create_train_val_split(data, val_ratio=0.15, seed=42)
    
    data.train_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
    data.val_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
    data.train_mask[data.train_idx] = True
    data.val_mask[data.val_idx] = True
    
    d_in = data.x.shape[1]
    d_out = len(torch.unique(data.y))
    data = data.to(DEVICE)
    
    print(f"特征维度: {d_in}, 类别数: {d_out}", flush=True)
    
    # 分析训练数据分布
    train_labels = data.y[data.train_mask].cpu().numpy()
    print("训练集标签分布:", flush=True)
    label_cnt = Counter(train_labels)
    for l in sorted(label_cnt.keys()):
        print(f"  标签{l}: {label_cnt[l]}个 ({label_cnt[l]/len(train_labels)*100:.1f}%)", flush=True)
    
    # 使用GCN + 早停策略
    print("\n训练GCN模型...", flush=True)
    model = GCN(d_in, 256, d_out).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    
    best_val_acc = 0
    best_state = None
    patience = 0
    
    for epoch in range(200):
        model.train()
        optimizer.zero_grad()
        
        out = model(data.x, data.edge_index)
        loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
        
        model.eval()
        with torch.no_grad():
            pred = model(data.x, data.edge_index).argmax(dim=1)
            train_acc = accuracy_score(data.y[data.train_mask].cpu(), pred[data.train_mask].cpu())
            val_acc = accuracy_score(data.y[data.val_mask].cpu(), pred[data.val_mask].cpu())
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_state = model.state_dict().copy()
            patience = 0
        else:
            patience += 1
        
        if epoch % 20 == 0:
            print(f"Epoch {epoch:3d} | Loss: {loss.item():.4f} | Train: {train_acc:.4f} | Val: {val_acc:.4f}", flush=True)
        
        if patience >= 30:
            print(f"早停于 epoch {epoch}", flush=True)
            break
    
    model.load_state_dict(best_state)
    model.eval()
    
    with torch.no_grad():
        test_pred = model(data.x, data.edge_index).argmax(dim=1)[data.test_idx].cpu().numpy()
    
    # 保存
    raw = np.load('./data/A分类/A1.npz')
    sub = pd.DataFrame({'test_idx': raw['test_idx'], 'label': test_pred})
    sub.to_csv('./output/submission/A1.csv', index=False)
    
    print(f"\n验证准确率: {best_val_acc:.4f}", flush=True)
    
    # 预测分布
    test_dist = Counter(test_pred)
    print("\n测试集预测分布:", flush=True)
    for l in sorted(test_dist.keys()):
        print(f"  标签{l}: {test_dist[l]}个 ({test_dist[l]/len(test_pred)*100:.1f}%)", flush=True)
    
    return best_val_acc

def train_recommendation():
    """产品推荐任务 - 改进版"""
    print("\n=== 产品推荐任务 A2 ===", flush=True)
    
    train_df = pd.read_csv('./data/A推荐/train.csv')
    test_df = pd.read_csv('./data/A推荐/test.csv')
    user_df = pd.read_csv('./data/A推荐/user.csv')
    item_df = pd.read_csv('./data/A推荐/item.csv')
    
    print(f"Train: {len(train_df)}, Test: {len(test_df)}, Items: {len(item_df)}", flush=True)
    
    # 编码
    item_encoder = LabelEncoder()
    item_encoder.fit(item_df['iid'])
    
    user_df['uid_idx'] = LabelEncoder().fit_transform(user_df['uid'])
    item_df['iid_idx'] = item_encoder.transform(item_df['iid'])
    
    train_df['uid_idx'] = user_df.set_index('uid')['uid_idx'].reindex(train_df['uid']).values
    train_df['target_idx'] = item_encoder.transform(train_df['target_iid'])
    test_df['uid_idx'] = user_df.set_index('uid')['uid_idx'].reindex(test_df['uid']).values
    
    # 处理缺失值
    train_df = train_df.dropna()
    test_df = test_df.dropna()
    
    # 特征
    user_feat = torch.from_numpy(StandardScaler().fit_transform(
        user_df.drop(['uid', 'uid_idx'], axis=1).fillna(0).values.astype(np.float32)
    )).float().to(DEVICE)
    
    item_feat = torch.from_numpy(StandardScaler().fit_transform(
        item_df.drop(['iid', 'iid_idx'], axis=1).fillna(0).values.astype(np.float32)
    )).float().to(DEVICE)
    
    class RecModel(torch.nn.Module):
        def __init__(self, u_dim, i_dim, h=64):
            super().__init__()
            self.u_emb = torch.nn.Embedding(user_feat.shape[0], h)
            self.i_emb = torch.nn.Embedding(item_feat.shape[0], h)
            self.u_net = torch.nn.Sequential(torch.nn.Linear(u_dim + h, h), torch.nn.ReLU())
            self.i_net = torch.nn.Sequential(torch.nn.Linear(i_dim + h, h), torch.nn.ReLU())
            self.score = torch.nn.Linear(h * 2, 1)
        
        def forward(self, u_idx, i_idx):
            u_cat = torch.cat([self.u_emb(u_idx), user_feat[u_idx]], dim=1)
            i_cat = torch.cat([self.i_emb(i_idx), item_feat[i_idx]], dim=1)
            u = self.u_net(u_cat)
            i = self.i_net(i_cat)
            return self.score(torch.cat([u, i], dim=1)).squeeze()
    
    model = RecModel(user_feat.shape[1], item_feat.shape[1]).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    print("训练推荐模型...", flush=True)
    for epoch in range(80):
        model.train()
        optimizer.zero_grad()
        
        idx = np.random.permutation(len(train_df))[:4096]
        u = torch.from_numpy(train_df['uid_idx'].values[idx].astype(int)).long().to(DEVICE)
        pos_i = torch.from_numpy(train_df['target_idx'].values[idx].astype(int)).long().to(DEVICE)
        neg_i = torch.from_numpy(np.random.randint(0, len(item_df), len(idx))).long().to(DEVICE)
        
        loss = -torch.mean(torch.log(torch.sigmoid(model(u, pos_i) - model(u, neg_i)) + 1e-8))
        loss.backward()
        optimizer.step()
        
        if epoch % 20 == 0:
            print(f"Epoch {epoch:3d} | Loss: {loss.item():.4f}", flush=True)
    
    # 预测
    model.eval()
    all_items = torch.arange(len(item_df)).long().to(DEVICE)
    preds = []
    
    print("生成推荐...", flush=True)
    for _, row in test_df.iterrows():
        uid = row['uid']
        u_idx = int(row['uid_idx'])
        
        with torch.no_grad():
            scores = model(torch.tensor([u_idx]).long().to(DEVICE).repeat(len(item_df)), all_items)
        
        top10 = torch.topk(scores, 10).indices.cpu().numpy()
        preds.append({'uid': uid, 'prediction': ','.join(item_encoder.inverse_transform(top10))})
    
    pd.DataFrame(preds).to_csv('./output/submission/A2.csv', index=False)
    print("A2完成!", flush=True)

def pack():
    with zipfile.ZipFile('./output/submission/prediction.zip', 'w') as zf:
        zf.write('./output/submission/A1.csv', 'A1.csv')
        zf.write('./output/submission/A2.csv', 'A2.csv')
    print("Created prediction.zip", flush=True)

if __name__ == '__main__':
    os.makedirs('./output/submission', exist_ok=True)
    val_acc = train_classification()
    train_recommendation()
    pack()
    print(f"\n=== 完成! Val Acc: {val_acc:.4f} ===", flush=True)