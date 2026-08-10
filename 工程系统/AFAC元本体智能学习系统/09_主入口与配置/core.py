"""
AFAC2026 核心模块整合
========================
整合了 LLM 客户端和 AutoML 智能体
"""

import os
import random
import json
import requests
import zipfile
import numpy as np
import pandas as pd
from typing import Optional, List, Dict, Any


# ====================== 全局配置（赛题硬性参数） ======================
TOTAL_BUDGET = 100
COST_PER_EXP = 10
MODEL_TYPES = ["mlp", "cnn", "transformer"]
LR_RANGE = [1e-5, 1e-2]
BATCH_RANGE = [16, 128]
WD_RANGE = [1e-6, 1e-3]
EPOCH_RANGE = [10, 100]


# ====================== LLM 客户端 ======================
class LLMClient:
    """LLM Client using DashScope API (compatible with OpenAI format)"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = "qwen-plus",
        timeout: int = 60
    ):
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = base_url or os.getenv(
            "LLM_BASE_URL", 
            "https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.model = model
        self.timeout = timeout
        
        if not self.api_key:
            raise ValueError("API key is required. Set LLM_API_KEY env var.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(
        self,
        system_prompt: str = "",
        user_message: str = "",
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Send a chat request to the LLM."""
        if messages is None:
            messages = []
        
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        
        if user_message:
            messages.append({"role": "user", "content": user_message})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        url = f"{self.base_url}/chat/completions"
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return str(result)
                
        except requests.exceptions.RequestException as e:
            return f"Request error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"


# ====================== 仿真实验环境 ======================
def run_simulation_exp(model_type, lr, batch_size, weight_decay, epochs):
    """模拟跑完一整轮实验，仅返回最终val_score（稀疏反馈）"""
    base_score = 0.6
    if model_type == "transformer":
        base_score += 0.15
    elif model_type == "cnn":
        base_score += 0.08
    lr_opt = abs(np.log10(lr) + 3)
    wd_opt = abs(np.log10(weight_decay) + 4)
    noise = random.uniform(-0.05, 0.05)
    val_score = base_score - 0.02*lr_opt - 0.01*wd_opt + noise
    return round(max(min(val_score, 0.98), 0.1), 4)


# ====================== 内在奖励模块 ======================
def get_intrinsic_reward(history, current_score):
    """基于历史轨迹得分差生成伪密集内在奖励"""
    if len(history) == 0:
        return 0.0
    mean_score = np.mean([h["final_score"] for h in history])
    return current_score - mean_score


# ====================== AutoML 智能体 ======================
class AutoExperimentAgent:
    """简易分层智能体：上层离散选型 + 下层连续超参"""
    
    def __init__(self, explore_rate=0.6):
        self.explore_rate = explore_rate

    def sample_config(self, history):
        # 上层：模型选型（探索/利用）
        if random.random() < self.explore_rate:
            model_type = random.choice(MODEL_TYPES)
        else:
            if len(history) > 0:
                best = max(history, key=lambda x: x["final_score"])
                model_type = best["model_type"]
            else:
                model_type = random.choice(MODEL_TYPES)
        
        # 下层：连续超参随机采样
        lr = np.random.uniform(*LR_RANGE)
        batch_size = int(np.random.uniform(*BATCH_RANGE))
        weight_decay = np.random.uniform(*WD_RANGE)
        epochs = int(np.random.uniform(*EPOCH_RANGE))
        
        return {
            "model_type": model_type,
            "lr": round(lr, 6),
            "batch_size": batch_size,
            "weight_decay": round(weight_decay, 6),
            "epochs": epochs
        }


# ====================== 主迭代循环 ======================
def run_auto_experiment(
    total_budget: int = TOTAL_BUDGET,
    cost_per_exp: int = COST_PER_EXP,
    output_dir: str = "output"
) -> Dict[str, Any]:
    """运行自动实验迭代"""
    trajectory_records = []
    best_exp_record = None
    current_step = 1
    remain_budget = total_budget
    agent = AutoExperimentAgent()
    
    while remain_budget >= cost_per_exp:
        cfg = agent.sample_config(trajectory_records)
        score = run_simulation_exp(**cfg)
        remain_budget -= cost_per_exp
        
        record = {
            "step": current_step,
            "action_config": json.dumps(cfg),
            "consume_budget": cost_per_exp,
            "final_score": score
        }
        trajectory_records.append(record)
        
        if best_exp_record is None or score > best_exp_record["final_score"]:
            best_exp_record = {
                "exp_id": current_step,
                "model_type": cfg["model_type"],
                "lr": cfg["lr"],
                "batch_size": cfg["batch_size"],
                "weight_decay": cfg["weight_decay"],
                "epochs": cfg["epochs"],
                "val_score": score
            }
        
        intr_reward = get_intrinsic_reward(trajectory_records[:-1], score)
        print(f"Step{current_step} | Score:{score} | IntrinsicReward:{round(intr_reward,4)}")
        
        agent.explore_rate = max(0.05, agent.explore_rate - 0.02)
        current_step += 1
    
    # 保存结果
    os.makedirs(output_dir, exist_ok=True)
    best_df = pd.DataFrame([best_exp_record])
    best_df.to_csv(f"{output_dir}/最优实验配置结果.csv", index=False, encoding="utf-8")
    
    traj_df = pd.DataFrame(trajectory_records)
    traj_df.to_csv(f"{output_dir}/Agent全轮决策轨迹.csv", index=False, encoding="utf-8")
    
    return {
        "trajectory": trajectory_records,
        "best": best_exp_record,
        "total_steps": current_step - 1
    }


# ====================== 提交文件生成 ======================
def generate_submission(
    output_dir: str = "output/submission",
    num_a1: int = 2751,
    num_a2: int = 10000,
    num_classes: int = 10,
    item_pool_size: int = 10000,
    top_k: int = 10
) -> str:
    """生成 A1.csv 和 A2.csv 提交文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    # A1.csv: 分类任务
    a1_data = {
        'test_idx': list(range(num_a1)),
        'label': [random.randint(0, num_classes - 1) for _ in range(num_a1)]
    }
    a1_df = pd.DataFrame(a1_data)
    a1_path = f"{output_dir}/A1.csv"
    a1_df.to_csv(a1_path, index=False, encoding="utf-8")
    
    # A2.csv: 推荐任务
    item_pool = list(range(item_pool_size))
    a2_data = {
        'uid': list(range(num_a2)),
        'prediction': [','.join(map(str, random.sample(item_pool, top_k))) for _ in range(num_a2)]
    }
    a2_df = pd.DataFrame(a2_data)
    a2_path = f"{output_dir}/A2.csv"
    a2_df.to_csv(a2_path, index=False, encoding="utf-8")
    
    # 打包
    zip_path = f"{output_dir}/prediction.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(a1_path, arcname="A1.csv")
        zipf.write(a2_path, arcname="A2.csv")
    
    return zip_path


# ====================== 入口 ======================
if __name__ == "__main__":
    print("===== AFAC2026 自动实验系统 =====")
    
    # 运行实验
    result = run_auto_experiment()
    print(f"\n实验完成，共 {result['total_steps']} 轮")
    print(f"最优配置: {result['best']}")
    
    # 生成提交文件
    zip_path = generate_submission()
    print(f"\n提交文件已打包: {zip_path}")
