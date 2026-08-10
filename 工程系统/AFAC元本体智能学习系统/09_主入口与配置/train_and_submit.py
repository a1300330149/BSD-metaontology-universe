import torch
import torch.nn.functional as F
import numpy as np
import pandas as pd
import os
import sys
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics import accuracy_score
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.afac2026_data_loader import load_afac2026_real_data, create_train_val_split, normalize_graph_features
from src.entity_layer.models import GCN, GAT, DeepGCN, GATv2

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"使用设备: {DEVICE}")

def train_gnn_classifier():
    """训练产品分类任务的GNN模型"""
    print("\n=== 产品分类任务（A1）===")
    
    data = load_afac2026_real_data('./data/A分类/A1.npz')
    data = normalize_graph_features(data)
    data = create_train_val_split(data, val_ratio=0.15, seed=42)
    
    data.train_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
    data.val_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
    data.train_mask[data.train_idx] = True
    data.val_mask[data.val_idx] = True
    
    d_in = data.x.shape[1]
    d_h = 256
    d_out = len(torch.unique(data.y))
    
    model = DeepGCN(d_in, d_h, d_out, num_layers=8).to(DEVICE)
    data = data.to(DEVICE)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=5e-4)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)
    
    best_val_acc = 0
    patience = 0
    max_patience = 30
    
    print(f"\n模型参数: {sum(p.numel() for p in model.parameters())}")
    print(f"训练开始...")
    
    for epoch in range(200):
        model.train()
        optimizer.zero_grad()
        
        out = model(data.x, data.edge_index)
        loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask])
        
        loss.backward()
        optimizer.step()
        scheduler.step()
        
        model.eval()
        with torch.no_grad():
            out = model(data.x, data.edge_index)
            pred = out.argmax(dim=1)
            
            train_acc = accuracy_score(data.y[data.train_mask].cpu().numpy(), pred[data.train_mask].cpu().numpy())
            val_acc = accuracy_score(data.y[data.val_mask].cpu().numpy(), pred[data.val_mask].cpu().numpy())
            
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), './output/submission/best_a1_model.pt')
            patience = 0
        else:
            patience += 1
            
        if epoch % 10 == 0:
            print(f"Epoch {epoch:3d} | Loss: {loss.item():.4f} | Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")
            
        if patience >= max_patience:
            print(f"早停于 epoch {epoch}")
            break
    
    model.load_state_dict(torch.load('./output/submission/best_a1_model.pt'))
    model.eval()
    
    with torch.no_grad():
        out = model(data.x, data.edge_index)
        test_pred = out.argmax(dim=1)[data.test_idx].cpu().numpy()
    
    raw_data = np.load('./data/A分类/A1.npz')
    real_test_idx = raw_data['test_idx']
    
    submission = pd.DataFrame({
        'test_idx': real_test_idx,
        'label': test_pred
    })
    
    submission.to_csv('./output/submission/A1.csv', index=False)
    print(f"\nA1.csv 已保存，验证集最佳准确率: {best_val_acc:.4f}")
    
    unique, counts = np.unique(test_pred, return_counts=True)
    print("预测标签分布:")
    for label, count in zip(unique, counts):
        print(f"  标签{label}: {count}个 ({count/len(test_pred)*100:.2f}%)")

def train_recommendation():
    """训练产品推荐任务"""
    print("\n\n=== 产品推荐任务（A2）===")
    
    train_df = pd.read_csv('./data/A推荐/train.csv')
    test_df = pd.read_csv('./data/A推荐/test.csv')
    user_df = pd.read_csv('./data/A推荐/user.csv')
    item_df = pd.read_csv('./data/A推荐/item.csv')
    
    print(f"训练集: {len(train_df)}")
    print(f"测试集: {len(test_df)}")
    print(f"用户数: {len(user_df)}")
    print(f"商品数: {len(item_df)}")
    
    user_encoder = LabelEncoder()
    item_encoder = LabelEncoder()
    
    all_items = list(item_df['iid'].unique())
    item_encoder.fit(all_items)
    
    user_df['uid_idx'] = user_encoder.fit_transform(user_df['uid'])
    item_df['iid_idx'] = item_encoder.transform(item_df['iid'])
    
    train_df['uid_idx'] = user_encoder.transform(train_df['uid'])
    train_df['target_idx'] = item_encoder.transform(train_df['target_iid'])
    
    test_df['uid_idx'] = user_encoder.transform(test_df['uid'])
    
    user_features = user_df.drop(['uid', 'uid_idx'], axis=1).values
    item_features = item_df.drop(['iid', 'iid_idx'], axis=1).values
    
    scaler_u = MinMaxScaler()
    scaler_i = MinMaxScaler()
    user_features = scaler_u.fit_transform(user_features)
    item_features = scaler_i.fit_transform(item_features)
    
    user_features = torch.from_numpy(user_features).float().to(DEVICE)
    item_features = torch.from_numpy(item_features).float().to(DEVICE)
    
    class RecommendationModel(torch.nn.Module):
        def __init__(self, user_dim, item_dim, hidden_dim=128):
            super().__init__()
            self.user_mlp = torch.nn.Sequential(
                torch.nn.Linear(user_dim, hidden_dim),
                torch.nn.ReLU(),
                torch.nn.BatchNorm1d(hidden_dim),
                torch.nn.Linear(hidden_dim, hidden_dim),
                torch.nn.ReLU()
            )
            self.item_mlp = torch.nn.Sequential(
                torch.nn.Linear(item_dim, hidden_dim),
                torch.nn.ReLU(),
                torch.nn.BatchNorm1d(hidden_dim),
                torch.nn.Linear(hidden_dim, hidden_dim),
                torch.nn.ReLU()
            )
            self.interaction = torch.nn.Sequential(
                torch.nn.Linear(hidden_dim * 2, hidden_dim),
                torch.nn.ReLU(),
                torch.nn.Linear(hidden_dim, 1)
            )
        
        def forward(self, u_idx, i_idx):
            u_feat = self.user_mlp(user_features[u_idx])
            i_feat = self.item_mlp(item_features[i_idx])
            concat = torch.cat([u_feat, i_feat], dim=1)
            return self.interaction(concat).squeeze()
    
    model = RecommendationModel(user_features.shape[1], item_features.shape[1]).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    print(f"\n训练推荐模型...")
    
    for epoch in range(50):
        model.train()
        optimizer.zero_grad()
        
        idx = np.random.permutation(len(train_df))[:8192]
        batch_u = torch.from_numpy(train_df['uid_idx'].values[idx]).long().to(DEVICE)
        batch_pos_i = torch.from_numpy(train_df['target_idx'].values[idx]).long().to(DEVICE)
        
        neg_idx = np.random.randint(0, len(item_df), len(idx))
        batch_neg_i = torch.from_numpy(neg_idx).long().to(DEVICE)
        
        pos_score = model(batch_u, batch_pos_i)
        neg_score = model(batch_u, batch_neg_i)
        
        loss = -torch.mean(torch.log(torch.sigmoid(pos_score - neg_score) + 1e-8))
        
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f"Epoch {epoch:3d} | Loss: {loss.item():.4f}")
    
    model.eval()
    all_item_idx = torch.arange(len(item_df)).long().to(DEVICE)
    
    print("\n生成推荐结果...")
    predictions = []
    
    for _, row in test_df.iterrows():
        uid = row['uid']
        uid_idx = row['uid_idx']
        
        uid_tensor = torch.tensor([uid_idx]).long().to(DEVICE).repeat(len(item_df))
        
        with torch.no_grad():
            scores = model(uid_tensor, all_item_idx)
        
        top10_idx = torch.topk(scores, 10).indices.cpu().numpy()
        top10_items = item_encoder.inverse_transform(top10_idx)
        
        predictions.append({
            'uid': uid,
            'prediction': ','.join(top10_items)
        })
    
    sub_df = pd.DataFrame(predictions)
    sub_df.to_csv('./output/submission/A2.csv', index=False)
    print(f"A2.csv 已保存")

def create_submission_zip():
    """创建提交压缩包"""
    import zipfile
    
    with zipfile.ZipFile('./output/submission/prediction.zip', 'w') as zf:
        zf.write('./output/submission/A1.csv', 'A1.csv')
        zf.write('./output/submission/A2.csv', 'A2.csv')
    
    print(f"\nprediction.zip 已创建")

if __name__ == '__main__':
    os.makedirs('./output/submission', exist_ok=True)
    
    train_gnn_classifier()
    train_recommendation()
    create_submission_zip()
    
    print("\n=== 提交文件准备完成 ===")
    print("文件位置: ./output/submission/prediction.zip")
    print("包含: A1.csv (产品分类), A2.csv (产品推荐)")