# -*- coding: utf-8 -*-
# ======================================================
# 归属: 2重·三界秩序基底
# 对应公理: 秩序守恒, 因果闭环
# ======================================================
"""
归属基底：第相变演化位（第三位）·自然秩序
对应三界秩序：自然秩序
对应公理：第2条（全域九维法理公理）、第5条（科研动力学公理）、第6条（相变临界公理）、第7条（递归自指公理）
对应九维维度：载体实体/相变自然/肉身能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：E1=0.35, E2=0.65, E3=0.90, γ=0.92
"""

import torch
import torch.nn as nn
from typing import Dict, Optional, Any, Union
from pathlib import Path

try:
    from src.entity_layer.models import MLP, GCN, GAT, TGN, DeepGCN, GATv2, GCNII, GraphTransformer
    from src.entity_layer.models_ext import GraphReg, GraphSeg, TextGNN, ImageGNN
    from src.utils.data_utils import evaluate
    import torch.optim.lr_scheduler as lr_scheduler
except ImportError as e:
    raise ImportError(f"Failed to import dependencies: {e}")


class BaseGraphAgent:
    """
    功能：基础图智能体，统摄所有图神经网络模型
    理论映射：2重自然秩序基底·实体演化核心规则
    能级关联：肉身能级e_body更新
    约束来源：科研动力学公理+相变临界公理
    """

    def __init__(self, dataset_config: Dict[str, Any], model_type: str = "GAT"):
        """
        初始化图智能体
        参数：
            dataset_config: 数据集配置，包含 feat_dim, hidden_dim, num_classes 等
            model_type: 模型类型，可选值：MLP, GCN, GAT, TGN, DeepGCN, GATv2, GCNII, GraphTransformer, GraphReg, GraphSeg, TextGNN, ImageGNN
        """
        self.dataset_config = dataset_config
        self.model_type = model_type
        self.model: Optional[nn.Module] = None
        self.optimizer: Optional[torch.optim.Optimizer] = None
        self.criterion: nn.Module = nn.CrossEntropyLoss()
        self.baseline_score: float = 0.0
        self.device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.current_data: Optional[Any] = None
        self.num_epochs_per_step: int = 10
        self.scheduler: Optional[lr_scheduler._LRScheduler] = None

    def init_base_model(
        self,
        lr: float = 0.001,
        wd: float = 1e-4,
        dropout: float = 0.3,
        hidden_dim: Optional[int] = None,
        num_layers: int = 3,
        num_heads: int = 4,
        data: Optional[Any] = None,
        pretrained_encoder: Optional[nn.Module] = None
    ) -> None:
        """
        初始化基础模型
        参数：
            lr: 学习率
            wd: 权重衰减
            dropout: dropout率（预留参数）
            hidden_dim: 隐藏层维度
            num_layers: 层数（仅部分模型使用）
            num_heads: 注意力头数（仅部分模型使用）
            data: 数据集对象，用于获取特征维度
            pretrained_encoder: 预训练编码器（预留参数）
        """
        if data is not None:
            if hasattr(data, 'x') and data.x is not None:
                d_in = data.x.shape[1]
                self.current_data = data
            else:
                raise ValueError("Data object must have 'x' attribute")
        else:
            d_in = self.dataset_config.get("feat_dim", 64)

        d_h = hidden_dim if hidden_dim is not None else self.dataset_config.get("hidden_dim", 128)
        d_out = self.dataset_config.get("num_classes", 10)

        model_map: Dict[str, Any] = {
            "MLP": MLP,
            "GCN": GCN,
            "GAT": GAT,
            "TGN": TGN,
            "DeepGCN": DeepGCN,
            "GATv2": GATv2,
            "GCNII": GCNII,
            "GraphTransformer": GraphTransformer,
            "GraphReg": GraphReg,
            "GraphSeg": GraphSeg,
            "TextGNN": TextGNN,
            "ImageGNN": ImageGNN,
        }

        model_cls = model_map.get(self.model_type, GAT)

        try:
            if self.model_type == "TGN":
                self.model = model_cls(d_in, d_h, d_out, self.dataset_config.get("num_nodes", 10000))
            elif self.model_type == "GraphReg":
                self.model = model_cls(d_in, d_h, d_out)
                self.criterion = nn.MSELoss()
            elif self.model_type == "GraphSeg":
                self.model = model_cls(d_in, d_h, d_out)
            elif self.model_type == "GCNII":
                self.model = model_cls(d_in, d_h, d_out, num_layers=num_layers)
            elif self.model_type == "DeepGCN":
                self.model = model_cls(d_in, d_h, d_out, num_layers=num_layers)
            elif self.model_type == "GATv2":
                self.model = model_cls(d_in, d_h, d_out, heads=num_heads)
            elif self.model_type == "GraphTransformer":
                self.model = model_cls(d_in, d_h, d_out, heads=num_heads)
            else:
                self.model = model_cls(d_in, d_h, d_out)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize model {self.model_type}: {e}")

        if pretrained_encoder is not None:
            self._load_pretrained_weights(pretrained_encoder, d_in, d_h)

        self.model.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr, weight_decay=wd)
        self.scheduler = lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=self.num_epochs_per_step, eta_min=lr * 0.01)

    def _load_pretrained_weights(self, encoder: nn.Module, d_in: int, d_h: int) -> None:
        """
        加载预训练权重
        参数：
            encoder: 预训练编码器
            d_in: 输入维度
            d_h: 隐藏维度
        """
        if encoder is None:
            return

        try:
            encoder_state = encoder.state_dict()
            model_state = self.model.state_dict()

            loaded_count = 0
            for encoder_key, encoder_val in encoder_state.items():
                if encoder_key in model_state:
                    model_val = model_state[encoder_key]
                    if model_val.shape == encoder_val.shape:
                        model_state[encoder_key].copy_(encoder_val)
                        loaded_count += 1

            if loaded_count > 0:
                self.model.load_state_dict(model_state)
            else:
                pass
        except Exception:
            pass

    def update_optimizer(self, lr: float = 0.001, wd: float = 1e-4) -> None:
        """
        更新优化器
        参数：
            lr: 新学习率
            wd: 新权重衰减
        """
        if self.model is None:
            raise RuntimeError("Model not initialized. Call init_base_model first.")

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr, weight_decay=wd)
        self.scheduler = lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=self.num_epochs_per_step, eta_min=lr * 0.01)

    def train_one_epoch(self, data: Any) -> float:
        """
        训练一个epoch
        参数：
            data: 训练数据
        返回：
            best_val: 最佳验证准确率
        """
        if self.model is None or self.optimizer is None:
            raise RuntimeError("Model or optimizer not initialized")

        data = data.to(self.device)
        best_val: float = 0.0

        for epoch in range(self.num_epochs_per_step):
            self.model.train()
            self.optimizer.zero_grad()

            try:
                if self.model_type == "TGN" and hasattr(data, "edge_time") and data.edge_time is not None:
                    out = self.model(data.x, data.edge_index, data.edge_time)
                else:
                    out = self.model(data.x, data.edge_index)
            except Exception as e:
                raise RuntimeError(f"Forward pass failed: {e}")

            loss = self.criterion(out[data.train_mask], data.y[data.train_mask])
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.optimizer.step()
            if self.scheduler is not None:
                self.scheduler.step()

            val_acc = evaluate(self.model, data, "val")
            if val_acc > best_val:
                best_val = val_acc
                if val_acc > self.baseline_score:
                    self.baseline_score = val_acc

        return best_val

    def get_entity_performance(self) -> float:
        """
        获取实体性能分数
        返回：
            baseline_score: 基线分数
        """
        return self.baseline_score

    def predict(self, data: Any) -> torch.Tensor:
        """
        预测
        参数：
            data: 数据
        返回：
            pred: 预测结果
        """
        if self.model is None:
            raise RuntimeError("Model not initialized")

        self.model.eval()
        data = data.to(self.device)

        with torch.no_grad():
            if self.model_type == "TGN" and hasattr(data, "edge_time") and data.edge_time is not None:
                out = self.model(data.x, data.edge_index, data.edge_time)
            else:
                out = self.model(data.x, data.edge_index)

        return out.argmax(dim=1)

    def test(self, data: Any) -> float:
        """
        测试模型性能
        参数：
            data: 测试数据
        返回：
            test_acc: 测试准确率
        """
        return evaluate(self.model, data, "test")

    def save_model(self, path: Union[str, Path]) -> None:
        """
        保存模型
        参数：
            path: 保存路径
        """
        if self.model is None:
            raise RuntimeError("Model not initialized")

        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict() if self.optimizer else None,
            'baseline_score': self.baseline_score,
            'model_type': self.model_type,
            'dataset_config': self.dataset_config,
        }, str(path))

    def load_model(self, path: Union[str, Path]) -> None:
        """
        加载模型
        参数：
            path: 模型路径
        """
        checkpoint = torch.load(str(path), map_location=self.device)
        self.model_type = checkpoint['model_type']
        self.dataset_config = checkpoint['dataset_config']

        self.init_base_model()
        self.model.load_state_dict(checkpoint['model_state_dict'])

        if checkpoint.get('optimizer_state_dict') and self.optimizer:
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

        self.baseline_score = checkpoint.get('baseline_score', 0.0)
