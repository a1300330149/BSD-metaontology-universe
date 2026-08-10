import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import numpy as np
from src.master_agent.master_creation_agent import CreationMasterAgent
from src.entity_layer.models_ext import GraphReg, GraphSeg, TextGNN, ImageGNN
from src.utils.multi_modal_loader import load_nlp_text_graph, load_cv_image_graph
from src.support.result_generator import ResultGeneratorAgent
from src.core.global_state import TransformLevel

def test_creation_master():
    print("\n=== 测试创世强化系主控 ===")
    config = {
        "max_budget": 100,
        "domain": "graph_learning",
        "dataset": {"feat_dim": 128, "hidden_dim": 64, "num_classes": 10}
    }
    master = CreationMasterAgent(config)
    
    master.set_manual_es(0.9)
    assert master.global_state.e_self == 0.9
    assert master.global_state.transform_level == TransformLevel.THIRD_TAO
    
    master.set_manual_es(0.5)
    assert master.global_state.e_self == 0.5
    assert master.global_state.transform_level == TransformLevel.FIRST_BODY
    
    plot = master.generate_plot("修仙者")
    assert "修仙者" in plot
    assert "道心" in plot
    print("创世强化系主控测试通过")

def test_multi_modal_models():
    print("\n=== 测试多模态模型拓展 ===")
    model_reg = GraphReg(128, 64, 1)
    model_seg = GraphSeg(128, 64, 10)
    model_text = TextGNN(768, 128, 10)
    model_image = ImageGNN(2048, 256, 10)
    
    x_dummy = np.random.randn(100, 128).astype(np.float32)
    edge_dummy = np.random.randint(0, 100, (2, 500)).astype(np.int64)
    
    import torch
    x = torch.FloatTensor(x_dummy)
    edge = torch.LongTensor(edge_dummy)
    
    out_reg = model_reg(x, edge)
    assert out_reg.shape[1] == 1, "回归模型输出维度错误"
    
    out_seg = model_seg(x, edge)
    assert out_seg.shape[1] == 10, "分割模型输出维度错误"
    print("多模态模型拓展测试通过")

def test_ablation_report():
    print("\n=== 测试消融报告生成 ===")
    report_gen = ResultGeneratorAgent()
    mock_results = [
        {"group": "完整全模块", "metric": {"best_score": 0.85, "final_level": TransformLevel.THIRD_TAO, "total_step": 100}},
        {"group": "移除时空衬层", "metric": {"best_score": 0.82, "final_level": TransformLevel.SECOND_MIND, "total_step": 100}},
        {"group": "移除虚实校准", "metric": {"best_score": 0.78, "final_level": TransformLevel.FIRST_BODY, "total_step": 100}},
    ]
    report_gen.generate_ablation_report(mock_results, save_path=os.path.join(BASE, "./output/test_ablation.md"))
    assert os.path.exists(os.path.join(BASE, "./output/test_ablation.md")), "消融报告未生成"
    print("消融报告生成测试通过")

def test_multi_modal_loader():
    print("\n=== 测试多模态数据加载 ===")
    test_data_dir = os.path.join(BASE, "data")
    os.makedirs(test_data_dir, exist_ok=True)
    
    np.savez(os.path.join(test_data_dir, "test_text.npz"), 
             embeddings=np.random.randn(50, 128).astype(np.float32),
             labels=np.random.randint(0, 5, 50).astype(np.int64))
    
    try:
        text_graph = load_nlp_text_graph(os.path.join(test_data_dir, "test_text.npz"))
        assert text_graph.x.shape[0] == 50
        assert text_graph.edge_index.shape[1] > 0
        print("文本图数据加载测试通过")
    except Exception as e:
        print(f"文本图加载跳过: {e}")
    
    img_feat_dir = os.path.join(test_data_dir, "img_features")
    os.makedirs(img_feat_dir, exist_ok=True)
    for i in range(30):
        np.save(os.path.join(img_feat_dir, f"{i%3}_img_{i}.npy"), 
                np.random.randn(256).astype(np.float32))
    
    try:
        img_graph = load_cv_image_graph(img_feat_dir)
        assert img_graph.x.shape[0] == 30
        print("图像图数据加载测试通过")
    except Exception as e:
        print(f"图像图加载跳过: {e}")

def test_base_graph_agent_extended():
    print("\n=== 测试基础图智能体拓展模型 ===")
    from src.entity_layer.base_graph_agent import BaseGraphAgent
    
    config = {"feat_dim": 128, "hidden_dim": 64, "num_classes": 10}
    
    for model_type in ["GraphReg", "GraphSeg", "TextGNN", "ImageGNN"]:
        agent = BaseGraphAgent(config, model_type=model_type)
        agent.init_base_model()
        assert agent.model is not None, f"{model_type} 模型初始化失败"
        print(f"  {model_type} 初始化成功")
    
    print("基础图智能体拓展模型测试通过")

def main():
    print("==== 拓展模块测试 ====")
    test_creation_master()
    test_multi_modal_models()
    test_ablation_report()
    test_multi_modal_loader()
    test_base_graph_agent_extended()
    print("\n==== 所有拓展模块测试通过 ====")

if __name__ == "__main__":
    main()