"""
A1分类任务优化训练脚本
- 8头GAT注意力
- 残差连接
- 标签平滑
- 余弦退火学习率
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch_geometric.nn import GATConv
from torch_geometric.data import Data
from torch_geometric.utils import from_scipy_sparse_matrix
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split
import pandas as pd

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

# ====================== 划分训练/验证集 ======================
tr_idx, val_idx = train_test_split(
    train_idx,
    test_size=0.2,
    random_state=SEED,
    stratify=labels[train_idx]
)

print(f"训练集: {len(tr_idx)}, 验证集: {len(val_idx)}, 测试集: {len(test_idx)}")

# ====================== 转换为PyG格式 ======================
edge_index, edge_weight = from_scipy_sparse_matrix(adj)
x = torch.FloatTensor(features.todense())
y = torch.LongTensor(labels)

# ====================== 优化后的GAT模型 ======================
class GATClassifierV2(nn.Module):
    def __init__(self, in_dim, hidden_dim, num_classes, heads=8, dropout=0.4):
        super().__init__()
        self.conv1 = GATConv((in_dim, in_dim), hidden_dim, heads=heads, dropout=dropout)
        self.conv2 = GATConv((hidden_dim * heads, hidden_dim * heads), hidden_dim, heads=1, concat=False, dropout=dropout)
        
        self.res_fc = nn.Linear(in_dim, hidden_dim)
        
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, num_classes)
        )
        
        self.dropout = dropout
        
    def forward(self, x, edge_index, edge_weight=None):
        x1 = self.conv1(x, edge_index, edge_weight)
        x1 = F.elu(x1)
        x1 = F.dropout(x1, p=self.dropout, training=self.training)
        
        x2 = self.conv2(x1, edge_index, edge_weight)
        x2 = F.elu(x2)
        x2 = F.dropout(x2, p=self.dropout, training=self.training)
        
        x_res = self.res_fc(x)
        x = x2 + x_res
        
        out = self.classifier(x)
        return out

# ====================== 训练 ======================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"使用设备: {device}")

model = GATClassifierV2(
    in_dim=data['attr_shape'][1],
    hidden_dim=256,
    num_classes=10,
    heads=8,
    dropout=0.4
).to(device)

# 标签平滑
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

criterion = LabelSmoothingCrossEntropy(num_classes=10, smoothing=0.1)
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=200, eta_min=1e-5)

# 训练循环
best_val_acc = 0
best_model = None

print("开始训练...")
for epoch in range(200):
    model.train()
    optimizer.zero_grad()
    
    out = model(x, edge_index, edge_weight)
    loss = criterion(out[tr_idx], y[tr_idx])
    loss.backward()
    optimizer.step()
    scheduler.step()
    
    # 验证
    model.eval()
    with torch.no_grad():
        out = model(x, edge_index, edge_weight)
        val_pred = out[val_idx].argmax(dim=1)
        val_acc = (val_pred == y[val_idx]).float().mean().item()
    
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        best_model = model.state_dict().copy()
        print(f"Epoch {epoch+1}: Val Acc = {val_acc:.4f} (Best)")
    
    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}: Loss = {loss.item():.4f}, Val Acc = {val_acc:.4f}")

print(f"\n最优验证准确率: {best_val_acc:.4f}")

# ====================== 测试 ======================
model.load_state_dict(best_model)
model.eval()
with torch.no_grad():
    out = model(x, edge_index, edge_weight)
    test_pred = out[test_idx].argmax(dim=1)
    
# 保存结果
result_df = pd.DataFrame({
    'test_idx': test_idx,
    'label': test_pred.numpy()
})
result_df.to_csv('output/submission/A1_improved.csv', index=False, encoding='utf-8')

print(f"✓ 已保存 A1_improved.csv")
print(f"  - 测试集准确率预期: {best_val_acc:.4f}")
print(f"  - 目标准确率: 0.68~0.72")

# 保存模型
torch.save(best_model, 'output/task1/best_model.pt')
print(f"✓ 已保存模型: output/task1/best_model.pt")