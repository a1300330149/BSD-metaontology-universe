import random
import json
import pandas as pd
import numpy as np
import os
import zipfile

# ====================== 全局配置（赛题硬性参数） ======================
TOTAL_BUDGET = 100        # 总算力预算
COST_PER_EXP = 10         # 单次实验消耗预算
MODEL_TYPES = ["mlp", "cnn", "transformer"]
# 连续超参搜索区间
LR_RANGE = [1e-5, 1e-2]
BATCH_RANGE = [16, 128]
WD_RANGE = [1e-6, 1e-3]
EPOCH_RANGE = [10, 100]

# 存储全部实验轨迹
trajectory_records = []
best_exp_record = None
current_step = 1
remain_budget = TOTAL_BUDGET

# ====================== 仿真实验环境（模拟官方评测接口） ======================
def run_simulation_exp(model_type, lr, batch_size, weight_decay, epochs):
    """模拟跑完一整轮实验，仅返回最终val_score（稀疏反馈，无中间信息）"""
    base_score = 0.6
    # 简单仿真打分逻辑，真实场景替换为官方环境接口调用
    if model_type == "transformer":
        base_score += 0.15
    elif model_type == "cnn":
        base_score += 0.08
    # 学习率正则扰动
    lr_opt = abs(np.log10(lr) + 3)
    wd_opt = abs(np.log10(weight_decay) + 4)
    noise = random.uniform(-0.05, 0.05)
    val_score = base_score - 0.02*lr_opt - 0.01*wd_opt + noise
    return round(max(min(val_score, 0.98), 0.1), 4)

# ====================== 内在奖励模块（解决稀疏反馈核心） ======================
def get_intrinsic_reward(history, current_score):
    """基于历史轨迹得分差生成伪密集内在奖励"""
    if len(history) == 0:
        return 0.0
    mean_score = np.mean([h["final_score"] for h in history])
    return current_score - mean_score

# ====================== 简易分层智能体（上层离散选型+下层连续超参） ======================
class AutoExperimentAgent:
    def __init__(self, explore_rate=0.6):
        self.explore_rate = explore_rate

    def sample_config(self, history):
        # 上层：模型选型（探索/利用）
        if random.random() < self.explore_rate:
            model_type = random.choice(MODEL_TYPES)
        else:
            # 利用历史最优模型
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
        cfg = {
            "model_type": model_type,
            "lr": round(lr, 6),
            "batch_size": batch_size,
            "weight_decay": round(weight_decay, 6),
            "epochs": epochs
        }
        return cfg

# ====================== 主迭代循环 ======================
if __name__ == "__main__":
    agent = AutoExperimentAgent()
    # 串行循环直到预算不足
    while remain_budget >= COST_PER_EXP:
        # 1. Agent生成超参配置
        cfg = agent.sample_config(trajectory_records)
        # 2. 执行实验，扣除预算
        score = run_simulation_exp(**cfg)
        remain_budget -= COST_PER_EXP
        # 3. 记录单条轨迹
        record = {
            "step": current_step,
            "action_config": json.dumps(cfg),
            "consume_budget": COST_PER_EXP,
            "final_score": score
        }
        trajectory_records.append(record)
        # 4. 更新最优实验
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
        # 5. 内在奖励更新Agent（此处仅示意，真实可接入RL网络更新）
        intr_reward = get_intrinsic_reward(trajectory_records[:-1], score)
        print(f"Step{current_step} | Score:{score} | IntrinsicReward:{round(intr_reward,4)} | RemainBudget:{remain_budget}")
        # 动态衰减探索率，预算越少越偏向利用
        agent.explore_rate = max(0.05, agent.explore_rate - 0.02)
        current_step += 1

    # ====================== 创建输出目录 ======================
    os.makedirs("output/submission", exist_ok=True)

    # ====================== 生成实验日志文件 ======================
    best_df = pd.DataFrame([best_exp_record])
    best_df.to_csv("output/最优实验配置结果.csv", index=False, encoding="utf-8")

    traj_df = pd.DataFrame(trajectory_records)
    traj_df.to_csv("output/Agent全轮决策轨迹.csv", index=False, encoding="utf-8")

    # ====================== 生成 A1.csv 和 A2.csv (Baseline 随机预测) ======================
    print("\n===== 生成 A榜提交文件 =====")
    
    # 生成 A1.csv (2751行, 任务1：分类，label 0~9)
    a1_data = {
        'test_idx': list(range(2751)),
        'label': [random.randint(0, 9) for _ in range(2751)]
    }
    a1_df = pd.DataFrame(a1_data)
    a1_path = "output/submission/A1.csv"
    a1_df.to_csv(a1_path, index=False, encoding="utf-8")
    print(f"已生成 {a1_path} (行数: {len(a1_df)})")

    # 生成 A2.csv (10000行, 任务2：推荐，每行10个item)
    # 假设 item 池为 0~9999，每行随机抽取 10 个不重复的 item
    item_pool = list(range(10000)) 
    a2_data = {
        'uid': list(range(10000)),
        'prediction': [','.join(map(str, random.sample(item_pool, 10))) for _ in range(10000)]
    }
    a2_df = pd.DataFrame(a2_data)
    a2_path = "output/submission/A2.csv"
    a2_df.to_csv(a2_path, index=False, encoding="utf-8")
    print(f"已生成 {a2_path} (行数: {len(a2_df)})")

    # ====================== 自动打包为 prediction.zip ======================
    zip_path = "output/prediction.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # arcname 确保压缩包内没有多余的目录层级，直接是 A1.csv 和 A2.csv
        zipf.write(a1_path, arcname="A1.csv")
        zipf.write(a2_path, arcname="A2.csv")
    
    print(f"\n===== 迭代完成，文件导出并打包成功 =====")
    print(f"1. output/最优实验配置结果.csv")
    print(f"2. output/Agent全轮决策轨迹.csv")
    print(f"3. {zip_path} (包含 A1.csv 和 A2.csv，可直接提交)")
    print("【重要】仅在平台Notebook内导出文件再提交，本地文件会报计算未配置！")
