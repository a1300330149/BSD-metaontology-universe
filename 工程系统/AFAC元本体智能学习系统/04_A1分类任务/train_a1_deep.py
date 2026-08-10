"""
A1分类任务深度优化训练脚本
- 图Transformer架构
- 自监督预训练
- 多模型集成学习
- 目标: 0.75+
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch_geometric.nn import GATConv, GCNConv, TransformerConv, global_mean_pool
from torch_geometric.data import Data
from torch_geometric.utils import from_scipy_sparse_matrix, to_undirected
from torch_geometric.transforms import RandomNodeSplit
from scipy.sparse import csr_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

# ====================== 加载数据 ======================
print("加载数据...")
data = np.load("data/A分类/A1.npz")

adj = csr_matrix(
    (data["adj_data"], data["adj_indices"], data["adj_indptr"]),
    shape=tuple(data["adj_shape"]),
)

features = csr_matrix(
    (data["attr_data"], data["attr_indices"], data["attr_indptr"]),
    shape=tuple(data["attr_shape"]),
)

labels = data["labels"]
train_idx = data["train_idx"]
test_idx = data["test_idx"]

print(f"节点数: {data['adj_shape'][0]}, 特征维度: {data['attr_shape'][1]}, 类别数: 10")

# ====================== 转换为PyG格式 ======================
edge_index, edge_weight = from_scipy_sparse_matrix(adj)
edge_index = to_undirected(edge_index)
x = torch.FloatTensor(features.todense())
y = torch.LongTensor(labels)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"使用设备: {device}")

# ====================== 图Transformer模型 ======================
class GraphTransformer(nn.Module):
    def __init__(self, in_dim, hidden_dim, num_classes, num_heads=4, num_layers=3, dropout=0.3):
        super().__init__()
        self.input_proj = nn.Linear(in_dim, hidden_dim)
        self.layers = nn.ModuleList()
        for _ in range(num_layers):
            self.layers.append(
                TransformerConv(hidden_dim, hidden_dim // num_heads, heads=num_heads, 
                              dropout=dropout)
            )
        self.norm_layers = nn.ModuleList([nn.LayerNorm(hidden_dim) for _ in range(num_layers)])
        self.residual_proj = nn.Linear(in_dim, hidden_dim)
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, num_classes)
        )
        self.dropout = dropout
        
    def forward(self, x, edge_index, edge_weight=None):
        x_res = self.residual_proj(x)
        x = self.input_proj(x)
        
        for layer, norm in zip(self.layers, self.norm_layers):
            x = x + layer(x, edge_index)
            x = norm(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
            
        x = x + x_res
        out = self.classifier(x)
        return out

# ====================== 深层GAT模型 ======================
class DeepGAT(nn.Module):
    def __init__(self, in_dim, hidden_dim, num_classes, heads=8, num_layers=3, dropout=0.3):
        super().__init__()
        self.convs = nn.ModuleList()
        self.convs.append(GATConv((in_dim, in_dim), hidden_dim, heads=heads, dropout=dropout))
        for _ in range(num_layers - 1):
            self.convs.append(GATConv((hidden_dim * heads, hidden_dim * heads), hidden_dim, 
                                     heads=heads, dropout=dropout))
        self.res_fc = nn.Linear(in_dim, hidden_dim * heads)
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * heads, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, num_classes)
        )
        self.dropout = dropout
        
    def forward(self, x, edge_index, edge_weight=None):
        x_res = self.res_fc(x)
        for conv in self.convs:
            x = conv(x, edge_index, edge_weight)
            x = F.gelu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        x = x + x_res
        out = self.classifier(x)
        return out

# ====================== GCNII模型 ======================
class GCNII(nn.Module):
    def __init__(self, in_dim, hidden_dim, num_classes, num_layers=6, dropout=0.3, alpha=0.1, theta=0.5):
        super().__init__()
        self.lin1 = nn.Linear(in_dim, hidden_dim)
        self.convs = nn.ModuleList()
        for i in range(num_layers):
            self.convs.append(GCNConv(hidden_dim, hidden_dim))
        self.alpha = alpha
        self.theta = theta
        self.classifier = nn.Linear(hidden_dim, num_classes)
        self.dropout = dropout
        
    def forward(self, x, edge_index, edge_weight=None):
        x = F.dropout(x, p=self.dropout, training=self.training)
        x0 = self.lin1(x)
        x = x0
        for i, conv in enumerate(self.convs):
            x = conv(x, edge_index, edge_weight)
            x = F.gelu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
            beta = self.theta / (i + 1)
            x = (1 - beta) * x + beta * x0
            x = self.alpha * x0 + (1 - self.alpha) * x
        out = self.classifier(x)
        return out

# ====================== 标签平滑损失 ======================
class LabelSmoothingCrossEntropy(nn.Module):
    def __init__(self, num_classes, smoothing=0.1):
        super().__init__()
        self.num_classes = num_classes
        self.smoothing = smoothing
        
    def forward(self, pred, target):
        log_prob = F.log_softmax(pred, dim=1)
        with torch.no_grad():
            smooth_target = torch.zeros_like(log_prob)
            smooth_target.fill_(self.smoothing / (self.num_classes - 1))
            smooth_target.scatter_(1, target.unsqueeze(1), 1 - self.smoothing)
        loss = (-smooth_target * log_prob).sum(dim=1).mean()
        return loss

# ====================== 训练单个模型 ======================
def train_model(model, x, edge_index, edge_weight, y, tr_idx, val_idx, epochs=200, lr=0.001):
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-5)
    criterion = LabelSmoothingCrossEntropy(num_classes=10, smoothing=0.1)
    
    best_val_acc = 0
    best_state = None
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        out = model(x, edge_index, edge_weight)
        loss = criterion(out[tr_idx], y[tr_idx])
        loss.backward()
        optimizer.step()
        scheduler.step()
        
        model.eval()
        with torch.no_grad():
            out = model(x, edge_index, edge_weight)
            val_pred = out[val_idx].argmax(dim=1)
            val_acc = (val_pred == y[val_idx]).float().mean().item()
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_state = model.state_dict().copy()
    
    return best_state, best_val_acc

# ====================== 集成学习 ======================
print("\n=== 开始集成学习训练 ===")

num_folds = 5
skf = StratifiedKFold(n_splits=num_folds, shuffle=True, random_state=SEED)

all_test_probs = []
all_models = []

for fold, (tr_idx, val_idx) in enumerate(skf.split(train_idx, labels[train_idx])):
    tr_idx = train_idx[tr_idx]
    val_idx = train_idx[val_idx]
    
    print(f"\n--- Fold {fold+1}/{num_folds} ---")
    
    # 模型1: 图Transformer
    model1 = GraphTransformer(
        in_dim=data['attr_shape'][1],
        hidden_dim=256,
        num_classes=10,
        num_heads=4,
        num_layers=3,
        dropout=0.3
    ).to(device)
    
    state1, acc1 = train_model(model1, x, edge_index, edge_weight, y, tr_idx, val_idx)
    print(f"  GraphTransformer: Val Acc = {acc1:.4f}")
    model1.load_state_dict(state1)
    model1.eval()
    with torch.no_grad():
        out1 = F.softmax(model1(x, edge_index, edge_weight), dim=1)
        all_test_probs.append(out1[test_idx].cpu().numpy())
    
    # 模型2: 深层GAT
    model2 = DeepGAT(
        in_dim=data['attr_shape'][1],
        hidden_dim=128,
        num_classes=10,
        heads=8,
        num_layers=3,
        dropout=0.3
    ).to(device)
    
    state2, acc2 = train_model(model2, x, edge_index, edge_weight, y, tr_idx, val_idx)
    print(f"  DeepGAT: Val Acc = {acc2:.4f}")
    model2.load_state_dict(state2)
    model2.eval()
    with torch.no_grad():
        out2 = F.softmax(model2(x, edge_index, edge_weight), dim=1)
        all_test_probs.append(out2[test_idx].cpu().numpy())
    
    # 模型3: GCNII
    model3 = GCNII(
        in_dim=data['attr_shape'][1],
        hidden_dim=256,
        num_classes=10,
        num_layers=6,
        dropout=0.3
    ).to(device)
    
    state3, acc3 = train_model(model3, x, edge_index, edge_weight, y, tr_idx, val_idx)
    print(f"  GCNII: Val Acc = {acc3:.4f}")
    model3.load_state_dict(state3)
    model3.eval()
    with torch.no_grad():
        out3 = F.softmax(model3(x, edge_index, edge_weight), dim=1)
        all_test_probs.append(out3[test_idx].cpu().numpy())

# ====================== 集成预测 ======================
print("\n=== 集成预测 ===")

weights = [0.4, 0.35, 0.25]
final_probs = np.zeros((len(test_idx), 10))

for i, (prob, weight) in enumerate(zip(all_test_probs, weights)):
    final_probs += prob * weight

test_pred = np.argmax(final_probs, axis=1)

# ====================== 保存结果 ======================
result_df = pd.DataFrame({
    'test_idx': test_idx,
    'label': test_pred
})
result_df.to_csv('output/submission/A1_deep.csv', index=False, encoding='utf-8')

print(f"\n✓ 已保存 A1_deep.csv")
print(f"  - 测试集预测完成")
print(f"  - 目标: 0.75+")

# 保存模型
torch.save({
    'models': ['GraphTransformer', 'DeepGAT', 'GCNII'],
    'weights': weights,
    'predictions': final_probs
}, 'output/task1/a1_deep_ensemble.pt')

print(f"✓ 已保存集成模型: output/task1/a1_deep_ensemble.pt")