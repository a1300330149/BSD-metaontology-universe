# -*- coding: utf-8 -*-
# ======================================================
# 归属: 2重·三界秩序基底
# 对应公理: 秩序守恒, 因果闭环
# ======================================================
"""
归属基底：第相变演化位（第三位）·自然秩序
对应三界秩序：自然秩序
对应公理：第2条（全域九维法理公理）、第5条（科研动力学公理）、第7条（递归自指公理）
对应九维维度：载体实体/相变自然/肉身能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：γ=0.92, τ=0.1(对比学习温度)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.utils import dropout_edge, mask_feature

class GCLAgent:
    """
    功能：图对比学习预训练智能体
    理论映射：2重自然秩序基底·实体自监督学习规则
    能级关联：肉身能级e_body更新
    约束来源：科研动力学公理
    """
    def __init__(self, encoder, hidden_dim=128, proj_dim=64, tau=0.1):
        self.encoder = encoder
        self.hidden_dim = hidden_dim
        self.proj_dim = proj_dim
        self.tau = tau
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.projection_head = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim * 2),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim * 2, proj_dim)
        ).to(self.device)
        
        self.encoder.to(self.device)
        self.optimizer = torch.optim.Adam(
            list(self.encoder.parameters()) + list(self.projection_head.parameters()),
            lr=0.001,
            weight_decay=1e-5
        )
        
    def augment(self, data):
        edge_index1, _ = dropout_edge(data.edge_index, p=0.2)
        x1, _ = mask_feature(data.x, p=0.2)
        
        edge_index2, _ = dropout_edge(data.edge_index, p=0.4)
        x2, _ = mask_feature(data.x, p=0.4)
        
        return x1, edge_index1, x2, edge_index2
    
    def sim(self, z1, z2):
        z1 = F.normalize(z1, dim=-1)
        z2 = F.normalize(z2, dim=-1)
        return torch.mm(z1, z2.t())
    
    def nt_xent_loss(self, z1, z2):
        f = lambda x: torch.exp(x / self.tau)
        
        refl_sim = f(self.sim(z1, z1))
        between_sim = f(self.sim(z1, z2))
        
        diag = torch.diag(refl_sim)
        pos = diag
        neg = refl_sim.sum(1) + between_sim.sum(1) - diag
        
        loss = -torch.log(pos / neg).mean()
        return loss
    
    def pretrain(self, data, epochs=200):
        self.encoder.train()
        self.projection_head.train()
        data = data.to(self.device)
        
        for epoch in range(epochs):
            self.optimizer.zero_grad()
            
            x1, edge_index1, x2, edge_index2 = self.augment(data)
            
            h1 = self.encoder(x1, edge_index1)
            h2 = self.encoder(x2, edge_index2)
            
            z1 = self.projection_head(h1)
            z2 = self.projection_head(h2)
            
            loss = self.nt_xent_loss(z1, z2)
            loss.backward()
            self.optimizer.step()
            
            if (epoch + 1) % 10 == 0:
                print(f"GCL预训练 Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")
        
        return loss.item()
    
    def get_pretrained_encoder(self):
        return self.encoder
    
    def save_encoder(self, path):
        torch.save(self.encoder.state_dict(), path)
        print(f"编码器已保存到: {path}")
    
    def load_encoder(self, path):
        self.encoder.load_state_dict(torch.load(path, map_location=self.device))
        print(f"编码器已从: {path} 加载")
