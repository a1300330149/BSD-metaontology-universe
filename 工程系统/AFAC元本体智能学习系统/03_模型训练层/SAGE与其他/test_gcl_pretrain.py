import sys
import os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import torch
import numpy as np
from src.utils.data_utils import load_afac_sparse_graph, normalize_graph_features
from src.entity_layer.gcl_agent import GCLAgent
from src.entity_layer.models import GCLEncoder, GCN
from src.utils.data_utils import evaluate

print("=== 测试GCL预训练 ===")
data_path = os.path.join(BASE, "data/afac2026_synth_graph_v3.npz")
data = load_afac_sparse_graph(data_path)
data = normalize_graph_features(data)

print(f"特征维度: {data.x.shape[1]}")

d_in = data.x.shape[1]
d_h = 128

encoder = GCLEncoder(d_in, d_h)
gcl_agent = GCLAgent(encoder, hidden_dim=d_h)

final_loss = gcl_agent.pretrain(data, epochs=50)
print(f"GCL预训练完成, 最终损失: {final_loss:.4f}")

pretrained_encoder = gcl_agent.get_pretrained_encoder()

model = GCN(d_in, d_h, 10)

encoder_state = pretrained_encoder.state_dict()
model_state = model.state_dict()

print("\n编码器参数:")
for key, val in encoder_state.items():
    print(f"  {key}: {val.shape}")

print("\n模型参数:")
for key, val in model_state.items():
    print(f"  {key}: {val.shape}")

if 'conv1.weight' in encoder_state and 'conv1.weight' in model_state:
    if model_state['conv1.weight'].shape == encoder_state['conv1.weight'].shape:
        print("\n✅ 形状匹配，可以加载预训练权重")
        model_state['conv1.weight'].copy_(encoder_state['conv1.weight'])
        model_state['conv1.bias'].copy_(encoder_state['conv1.bias'])
        model.load_state_dict(model_state)
        print("预训练权重加载成功")
    else:
        print(f"\n❌ 形状不匹配: 模型conv1={model_state['conv1.weight'].shape}, 编码器conv1={encoder_state['conv1.weight'].shape}")

model.to('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = torch.nn.CrossEntropyLoss()

data = data.to('cuda' if torch.cuda.is_available() else 'cpu')

print("\n=== 测试模型训练 ===")
for epoch in range(20):
    model.train()
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)
    loss = criterion(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 5 == 0:
        val_acc = evaluate(model, data, "val")
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}, Val Acc: {val_acc:.4f}")

test_acc = evaluate(model, data, "test")
print(f"\n测试准确率: {test_acc:.4f}")