
---
向量标签
---

# 基底层级标签
base_0:元道本源基底

# 公理标签
axiom_1:宿命双边界公理, axiom_2:自主科研闭环动力学公理, axiom_3:科研价值边际判定公理, axiom_4:选题创化生成机制, axiom_5:成果落地转化范式, axiom_6:全局宿命边界统摄理论, axiom_7:系统自进化迭代公理

# 九维维度标签
因果社会, 天道动力学

# 参数标签
- gamma: 0.92
- kappa: 0.35
- alpha: 0.18
- E1: 0.35
- E2: 0.65
- E3: 0.9

# 关键词标签
元本体, 双边界, 公理, 宿命, 舒适, 自然, 人道, 科研, 智能体, 能级

# 标签权重
1.0

# 标签时间
2026-06-23 13:05:07

# SHA256锁档哈希
e62f918340dc2975108294736ac8927d90584136972485931027958740925713

---

---
确权扉页
---

# 作品全称
V3.0 Rev.04 新四位一体框架3.0元本体论（专属理论分册）

# SHA256唯一锁档哈希
e62f918340dc2975108294736ac8927d90584136972485931027958740925713

# 作者/著作权人
杨腾飞（证件号码：433127199812193215）

# 锁档定稿日期
2026-06-20

# 三维协同确权
创世作者：杨腾飞（60%）
墨心推演：AI辅助（25%）
豆包运维：AI辅助（15%）

---

三阶智能决策系统（TO-IDS）工程化完整设计文档

阶段3 三阶智能决策系统（Third-Order Intelligent Decision System, TO-IDS）

工程化完整设计文档（承接阶段2 SOD-DBS，可直接交付代码落地）

阶段定位：整套自动科研系统的「道心决策层」，对应三阶道心觉醒阶段。在一阶实体拟合、二阶分布纠偏的能力基础上，构建完整的「实验记忆沉淀→智能寻优决策→复盘反思迭代→自主停止收敛」闭环，系统从“被动执行任务”升级为“主动规划科研、自主优化策略、全局管控预算”，是真正意义上全自动科研智能体的核心，也是赛题“有限预算下智能迭代、经验迁移”核心考点的完整落地。

理论溯源：人道三阶成长理论、因果社会系经验沉淀、创化社会系智能生成、时空嵌入升维理论、虚实二分校准机制、宿命/舒适双边界公理、六系六维流转动力学。

前置依赖：阶段0 OCE内核、阶段1 FO-EFS实体拟合系统、阶段2 SOD-DBS分布纠偏系统均已验收通过；三阶系统以决策层形式叠加于上层，仅通过标准API调用下层能力，不修改下层核心逻辑，保证架构解耦与稳态。



一、全局架构与接口规范

1. 模块层级关系

2. 命名空间规范

根包名：to_ids

所有模块通过 to_ids.adapter 调用下层系统与内核能力，禁止跨层直接访问内部实现

所有决策、策略、预估均标记为「主观幻相」，需经实相实验验证；所有实验结果、记忆数据标记为「实体实相」，开启写保护

全链路决策留痕，所有Agent行为可审计、可追溯、可复现

3. 全局枚举定义



二、模块一：下层系统适配层（TO-IDS Adapter）

理论溯源

对应「模态分划本体的层间交互与统摄规则」，三阶道心层统摄下层肉身、精神能力，通过标准化适配层统一调度所有下层能力，保证决策指令的准确执行与结果反馈。

核心职责

封装一、二阶系统所有对外能力，提供Agent决策调用的统一入口

统一透传OCE内核边界校验，所有决策执行前先过宿命边界

统一数据分类标记与虚实校准，所有实验结果自动沉淀入记忆库

统一日志审计，全决策链路可追溯、可复现

屏蔽下层系统细节，Agent只关注决策逻辑，不感知底层实现

核心函数伪代码

1. 单轮实验统一执行入口



三、模块二：实验记忆知识库（Experiment Memory Knowledge Base）

理论溯源

对应因果社会系时序经验沉淀，是Agent智能决策的唯一数据依据，所有历史实验结构化存储，支持时序加权、相似度检索、偏差统计、经验迁移，完全对应“因果轨迹沉淀”的理论设定。

核心职责

结构化存储全量历史实验数据，覆盖模型、超参、指标、偏置、偏差、耗时等全维度信息

支持多维度检索：时序加权检索、相似度检索、分任务检索、分阶段检索

自动统计虚实偏差规律、失效实验共性、优质经验特征

记忆数据标记为实体实相，开启写保护，禁止篡改历史实验

支持跨任务、跨数据集的经验复用与迁移

核心数据结构

核心函数伪代码

1. 实验记录入库

2. 时序加权相似检索

3. 偏差统计与规律归纳



四、模块三：智能寻优决策引擎（Intelligent Optimization Engine）

理论溯源

对应创化社会系智能生成+虚实二分校准，基于记忆库历史经验，自主生成高价值实验方案，替代低效的网格/随机搜索；同时通过虚实偏差修正预估收益，过滤低价值实验，最大化单轮预算收益率。

核心职责

支持多策略寻优：探索期随机采样、深耕期贝叶斯优化、收敛期多目标帕累托寻优

基于记忆库经验动态调整搜索空间与先验分布，提升寻优效率

内置幻相偏差校准：预估收益先做偏差修正，再判断是否值得执行

动态平衡探索与利用，匹配Agent成长阶段节奏

支持单目标与多目标两种寻优模式，适配不同任务需求

核心函数伪代码

1. 实验方案生成（含虚实校准）

2. 阶段探索率动态调度



五、模块四：复盘反思迭代模块（Reflection & Iteration Module）

理论溯源

对应三阶道心的自我觉醒与迭代能力，是Agent区别于普通AutoML工具的核心标志——定期复盘历史实验，总结失败规律、修正偏差认知、调整搜索空间、优化寻优策略，实现策略层面的自我进化，而非仅参数优化。

核心职责

定期自动触发复盘：按轮次间隔（如每10轮）或阶段切换时自动执行

失败实验归因分析：识别无效实验共性原因，剔除高失败率超参区间

虚实偏差修正：更新偏差统计，动态校准预估模型，减少幻相失真

搜索空间动态调整：收缩优质区间，剔除无效区间，提升寻优效率

阶段跃迁判断：基于成长指标自动判断是否进入下一阶位

核心函数伪代码

1. 全维度复盘执行

2. 三阶成长阶位自动判定



六、模块五：预算调度与自主停止器（Budget Scheduler & Auto-Stop）

理论溯源

对应宿命边界公理+舒适边界公理的全局管控，在有限预算约束下，动态分配各阶段资源，自主判断最优停止时机，避免无效迭代浪费预算，实现全局收益最大化。

核心职责

总预算全局管控：实时统计已用、剩余预算，严格不突破宿命边界

阶段预算动态分配：按成长阶段自动分配轮次资源，匹配三阶成长节奏

自主停止判断：基于边际收益、收敛状态、预算剩余，自动决定终止迭代

最优方案筛选：迭代结束后，从历史实验中筛选最优/最稳方案作为最终输出

多种子稳定性验证：收敛期自动执行多种子重复实验，验证方案鲁棒性

核心函数伪代码

1. 预算三阶段默认分配策略

2. 自主停止判断

3. 最终最优方案筛选



七、模块六：跨任务经验迁移引擎（Cross-Task Transfer Engine）

理论溯源

对应全学科统一基底+分形自相似法则，提取A任务沉淀的通用规律、超参先验、去偏范式，迁移适配到B任务，大幅降低新任务冷启动成本，是系统通用能力的核心体现，也是赛题“跨数据集可迁移经验”考点的直接落地。

核心职责

跨任务超参先验迁移：分类任务验证的最优超参区间，作为推荐任务寻优先验

稀疏处理范式迁移：分类任务的去偏、长尾增强方法，迁移到推荐冷启动场景

实验策略迁移：预算分配、探索节奏、复盘周期等通用策略跨任务复用

迁移效果自动评估：量化迁移带来的冷启动效率提升，持续优化迁移策略

核心函数伪代码



八、阶段3 对外统一API

核心全流程入口：一键全自动科研



九、阶段3 落地验收标准

完成代码开发后，满足以下全部条件即视为阶段3验收通过，标志三阶智能体闭环成型：

全自动闭环验证：给定数据集与预算，一键启动后全程零人工干预，自动完成全流程迭代，最终输出最优方案

寻优效率验证：相同120轮预算下，Agent自主迭代效果优于二阶网格/随机搜索15%以上，无效实验占比低于10%

阶段跃迁验证：可自动完成“探索→深耕→收敛”三阶阶段切换，切换时机与预算分配符合理论预期

复盘反思验证：每10轮自动复盘，可识别失败实验共性、动态收缩搜索空间，复盘后单轮实验平均收益提升

自主停止验证：可在预算耗尽前主动触发停止，边际收益不足时不浪费预算，停止时机准确率≥90%

经验迁移验证：分类任务经验迁移到推荐任务，冷启动前10轮平均收益提升≥30%，验证跨任务迁移有效性

边界合规验证：全程严格遵守宿命边界，无超预算、并行违规，所有操作可审计、可复现

赛题场景验证：针对赛题双任务，120轮预算内自动迭代至目标指标区间，生成合规提交文件



下一步推进说明

阶段3完成后，整套自动科研系统的核心智能闭环已全部成型，具备独立完成全流程科研任务的能力，可直接适配AFAC赛题三所有考点并形成差异化优势。后续将进入阶段4（跨域泛化系统），从单一AI任务扩展到全学科科研场景适配，进一步落地全学科统一基底与通用科研范式。

|（注：部分内容可能由 AI 生成）

| Plaintext
┌───────────────────────────────────────────────────────────────┐
│ 三阶智能决策系统 TO-IDS                                        │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐    │
│  │ 实验记忆 │ 智能寻优 │ 复盘反思 │ 预算调度 │ 跨域迁移 │    │
│  │ 知识库   │ 决策引擎 │ 模块     │ 器       │ 引擎     │    │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘    │
│                   三阶系统适配层                               │
└───────────────────────────────────────────────────────────────┘
        ↓ 统一调用二阶API
┌───────────────────────────────────────────────────────────────┐
│ 二阶分布纠偏系统 SOD-DBS                                      │
└───────────────────────────────────────────────────────────────┘
        ↓ 统一调用一阶API
┌───────────────────────────────────────────────────────────────┐
│ 一阶实体拟合系统 FO-EFS                                        │
└───────────────────────────────────────────────────────────────┘
        ↓ 统一调用OCE API
┌───────────────────────────────────────────────────────────────┐
│ 阶段0 元本体核心引擎 OCE                                      │
└───────────────────────────────────────────────────────────────┘ |
| --- |

| Python
from enum import Enum

class AgentStage(Enum):
    """Agent成长三阶阶段，对应人道三阶成长理论"""
    EXPLORATION = "exploration"    # 一阶探索期：广谱遍历，填充记忆库
    EXPLOITATION = "exploitation"  # 二阶深耕期：优质区间精细化寻优
    CONVERGENCE = "convergence"    # 三阶收敛期：稳定验证，输出最终结果

class SearchStrategy(Enum):
    """寻优策略类型"""
    RANDOM = "random"              # 随机采样（探索期）
    BAYESIAN_GP = "bayesian_gp"    # 高斯过程贝叶斯优化（深耕期）
    RL_DECISION = "rl_decision"    # 强化学习决策（收敛期）
    PARETO_MO = "pareto_mo"        # 多目标帕累托寻优

class ReflectionType(Enum):
    """反思类型"""
    FAILURE_ANALYSIS = "failure_analysis"    # 失败实验归因
    BIAS_CORRECTION = "bias_correction"      # 预估偏差修正
    SPACE_ADJUST = "space_adjust"            # 搜索空间调整
    STRATEGY_UPDATE = "strategy_update"      # 寻优策略更新 |
| --- |

| Python
def run_agent_experiment(dataset, model_name, hyper_params, debias_config=None) -> ExperimentResult:
    """
    Agent调度实验的统一入口
    1. 前置边界校验 2. 调用二阶去偏训练 3. 结果标记入记忆库 4. 返回实验结果
    """
    # 宿命边界校验：预算、并行、合规
    passed, msg = oce_adapter.hard_check({
        "budget_used": get_total_budget_used(),
        "parallel_count": 1
    })
    if not passed:
        raise RuntimeError(f"实验被宿命边界拦截: {msg}")
    
    # 调用二阶系统执行去偏实验
    result = sod_dbs_api.run_debiased_experiment(
        dataset, model_name, hyper_params, debias_config
    )
    
    # 结果自动沉淀入记忆库
    memory_knowledge_base.add_experiment(result)
    
    return result |
| --- |

| Python
class MemoryRecord:
    exp_id: str
    task_type: TaskType
    dataset_id: str
    model_name: str
    hyper_params: dict
    debias_config: dict
    stage_tag: AgentStage          # 所属成长阶段
    
    # 实相指标（真值，只读）
    val_accuracy: float            # 核心精度指标
    val_diversity: float           # 多样性指标
    val_fairness: float            # 公平性指标
    train_cost: float              # 算力/时间成本
    
    # 幻相指标（预估与偏差）
    pred_score: float              # 实验前预估值
    delta_illu: float              # 虚实偏差值
    confidence: float              # 预估置信度
    
    # 元信息
    timestamp: int
    is_valid: bool                 # 实验是否有效
    failure_reason: str            # 失败实验原因 |
| --- |

| Python
def add_experiment(result: ExperimentResult) -> None:
    """实验结果自动入库，标记实相只读"""
    record = MemoryRecord(
        exp_id = result.exp_id,
        task_type = result.task_type,
        hyper_params = result.hyper_params,
        val_accuracy = result.val_metrics["score"],
        val_diversity = result.val_metrics.get("diversity", 0),
        delta_illu = result.pred_result.delta_illu,
        is_valid = result.train_status == TrainStatus.FINISHED
    )
    _memory_pool.append(record)
    _memory_pool = freeze_readonly(_memory_pool)  # 实相写保护 |
| --- |

| Python
def retrieve_similar(target_params: dict, task_type: TaskType, top_k=5, gamma=0.9) -> list[MemoryRecord]:
    """
    时序加权相似检索：越近期、越相似的实验权重越高
    gamma: 时序衰减系数，对应时空嵌入时维τ衰减
    """
    # 计算超参相似度
    sim_scores = []
    for record in _memory_pool:
        if record.task_type != task_type or not record.is_valid:
            continue
        param_sim = calc_param_similarity(target_params, record.hyper_params)
        time_decay = gamma ** (current_time - record.timestamp)
        final_score = param_sim * time_decay
        sim_scores.append((final_score, record))
    
    sim_scores.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in sim_scores[:top_k]] |
| --- |

| Python
def get_illusion_bias_stats(task_type: TaskType) -> dict:
    """统计历史虚实偏差规律，用于修正预估，减少无效实验"""
    valid_records = [r for r in _memory_pool if r.task_type == task_type and r.is_valid]
    if not valid_records:
        return {"avg_delta": 0, "bias_trend": "flat"}
    
    avg_delta = np.mean([r.delta_illu for r in valid_records])
    bias_trend = calc_bias_trend(valid_records)
    return {
        "avg_delta_illu": avg_delta,
        "bias_trend": bias_trend,
        "high_bias_params": find_high_bias_params(valid_records)
    } |
| --- |

| Python
def generate_next_experiment(task_type: TaskType, search_space: dict, 
                             strategy: SearchStrategy, stage: AgentStage) -> dict:
    """
    生成下一组实验超参方案
    核心步骤：代理模型预估→虚实偏差修正→收益评估→输出最优方案
    """
    # 1. 基于历史记忆生成候选方案
    if strategy == SearchStrategy.RANDOM:
        candidates = sample_random_params(search_space, n=20)
    elif strategy == SearchStrategy.BAYESIAN_GP:
        history = memory_knowledge_base.get_valid_records(task_type)
        candidates = bayesian_gp_suggest(search_space, history, n=20)
    elif strategy == SearchStrategy.PARETO_MO:
        candidates = pareto_mo_suggest(search_space, history, n=20)
    else:
        raise ValueError("不支持的寻优策略")
    
    # 2. 虚实偏差校准：修正预估收益，过滤幻相高估
    bias_stats = memory_knowledge_base.get_illusion_bias_stats(task_type)
    for cand in candidates:
        pred_score = surrogate_model.predict(cand)
        # 用历史平均偏差修正预估
        corrected_score = pred_score - bias_stats["avg_delta_illu"]
        cand["corrected_score"] = corrected_score
        cand["pred_score"] = pred_score
    
    # 3. 过滤低价值方案，返回预期收益最高的一组
    candidates.sort(key=lambda x: x["corrected_score"], reverse=True)
    best_params = candidates[0]
    
    # 4. 探索率动态注入：按阶段概率替换为随机探索
    explore_rate = get_stage_explore_rate(stage)
    if np.random.random() < explore_rate:
        best_params = sample_random_params(search_space, n=1)[0]
    
    return best_params |
| --- |

| Python
def get_stage_explore_rate(stage: AgentStage) -> float:
    """
    对应相变自然层探索-利用相变规律
    探索期高探索、深耕期线性衰减、收敛期低探索
    """
    rate_map = {
        AgentStage.EXPLORATION: 0.8,
        AgentStage.EXPLOITATION: 0.3,
        AgentStage.CONVERGENCE: 0.1
    }
    return rate_map.get(stage, 0.5) |
| --- |

| Python
def run_reflection(task_type: TaskType, current_stage: AgentStage) -> dict:
    """
    执行一次完整复盘，输出修正后的策略配置
    对应道心层「反思→修正→进化」闭环
    """
    history = memory_knowledge_base.get_valid_records(task_type)
    if len(history) < 10:
        return {"action": "wait", "reason": "样本不足，暂不复盘"}
    
    reflection_result = {}
    
    # 1. 失败实验归因
    failure_records = [r for r in history if not r.is_valid]
    failure_patterns = analyze_failure_patterns(failure_records)
    reflection_result["failure_patterns"] = failure_patterns
    
    # 2. 虚实偏差更新
    new_bias_stats = recalculate_bias(history)
    reflection_result["updated_bias"] = new_bias_stats
    
    # 3. 搜索空间调整
    new_search_space = adjust_search_space(history, failure_patterns)
    reflection_result["new_search_space"] = new_search_space
    
    # 4. 阶段跃迁判断
    next_stage = check_stage_upgrade(history, current_stage)
    reflection_result["next_stage"] = next_stage
    
    log_audit(f"复盘完成，阶段: {current_stage.value} → {next_stage.value}")
    return reflection_result |
| --- |

| Python
def check_stage_upgrade(history: list, current_stage: AgentStage) -> AgentStage:
    """
    基于人道三阶成长阈值，自动判断是否阶位提升
    跃迁条件：记忆库规模、最优指标收敛度、无效实验占比
    """
    valid_count = len([r for r in history if r.is_valid])
    best_score = max([r.val_accuracy for r in history])
    recent_improve = calc_recent_improvement(history)
    invalid_ratio = 1 - valid_count / len(history)
    
    if current_stage == AgentStage.EXPLORATION:
        if valid_count >= 30 and invalid_ratio < 0.1:
            return AgentStage.EXPLOITATION
    elif current_stage == AgentStage.EXPLOITATION:
        if valid_count >= 90 and recent_improve < 0.01:
            return AgentStage.CONVERGENCE
    return current_stage |
| --- |

| Python
def get_stage_budget(total_budget: int) -> dict[AgentStage, int]:
    """
    对应120轮预算最优分配：探索25%、深耕50%、收敛25%
    匹配三阶成长节奏，可根据复盘结果动态微调
    """
    return {
        AgentStage.EXPLORATION: int(total_budget * 0.25),
        AgentStage.EXPLOITATION: int(total_budget * 0.5),
        AgentStage.CONVERGENCE: int(total_budget * 0.25)
    } |
| --- |

| Python
def should_stop(history: list, budget_left: int, stage: AgentStage) -> tuple[bool, str]:
    """
    自主判断是否终止迭代，触发条件：
    1. 预算耗尽 2. 连续多轮无提升 3. 收敛期稳定性达标
    """
    if budget_left <= 0:
        return True, "预算耗尽，宿命边界触发"
    
    if stage == AgentStage.CONVERGENCE:
        recent_gain = calc_recent_improvement(history, window=15)
        if recent_gain < 0.005 and budget_left < 10:
            return True, "指标已收敛，边际收益不足"
        
        stability = calc_stability(history, top_k=5)
        if stability > 0.99:
            return True, "方案已稳定，达到最优收敛状态"
    
    return False, "继续迭代" |
| --- |

| Python
def select_final_solution(history: list, mode="balanced") -> MemoryRecord:
    """
    从历史实验中筛选最终方案
    mode: accuracy=精度优先、diversity=多样性优先、balanced=均衡最优
    避免选单轮最高分，优先选连续稳定、方差小的方案
    """
    valid = [r for r in history if r.is_valid]
    if mode == "accuracy":
        return max(valid, key=lambda x: x.val_accuracy)
    elif mode == "diversity":
        return max(valid, key=lambda x: x.val_diversity)
    else:
        # 均衡模式：综合精度+多样性+稳定性
        scored = []
        for r in valid:
            score = 0.6 * normalize(r.val_accuracy) + 0.4 * normalize(r.val_diversity)
            scored.append((score, r))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] |
| --- |

| Python
def transfer_knowledge(source_task: TaskType, target_task: TaskType) -> dict:
    """
    从源任务向目标任务迁移可复用知识
    返回：初始搜索空间先验、默认去偏配置、预算策略建议
    """
    source_history = memory_knowledge_base.get_valid_records(source_task)
    if not source_history:
        return {"status": "no_source_data", "transfer_gain": 0}
    
    # 1. 超参先验迁移：提取源任务最优超参区间，缩小目标初始搜索范围
    optimal_params_range = extract_optimal_range(source_history)
    target_init_space = shrink_search_space(target_default_space, optimal_params_range)
    
    # 2. 去偏策略迁移：通用稀疏/不平衡处理范式直接复用
    common_debias = extract_common_debias_strategy(source_history)
    
    # 3. 实验策略迁移：预算分配、探索节奏通用
    budget_strategy = get_stage_budget(120)
    
    return {
        "init_search_space": target_init_space,
        "default_debias_config": common_debias,
        "budget_strategy": budget_strategy,
        "expected_cold_start_reduction": "30%"
    } |
| --- |

| Python
# to_ids/api.py 对外暴露
from .memory_base import add_experiment, retrieve_similar, get_bias_stats
from .optimization_engine import generate_next_experiment, SearchStrategy
from .reflection import run_reflection, check_stage_upgrade
from .budget_scheduler import should_stop, select_final_solution
from .transfer_engine import transfer_knowledge
from .agent_pipeline import run_full_auto_research
from .types import AgentStage |
| --- |

| Python
def run_full_auto_research(dataset, total_budget=120, target_mode="balanced") -> ExperimentResult:
    """
    全自动科研闭环：一键启动，全程零人工干预
    流程：初始化→探索期→复盘→深耕期→复盘→收敛期→停止→输出最优方案
    """
    stage = AgentStage.EXPLORATION
    strategy = SearchStrategy.RANDOM
    budget_used = 0
    
    while budget_used < total_budget:
        # 生成下一组实验方案
        params = generate_next_experiment(dataset.task_type, search_space, strategy, stage)
        # 执行实验
        result = adapter.run_agent_experiment(dataset, model_name, params)
        budget_used += 1
        
        # 定期复盘与阶段切换
        if budget_used % 10 == 0:
            reflection = run_reflection(dataset.task_type, stage)
            if reflection["next_stage"] != stage:
                stage = reflection["next_stage"]
                strategy = map_stage_to_strategy(stage)
        
        # 自主停止判断
        stop, reason = should_stop(memory_base.all_records(), total_budget - budget_used, stage)
        if stop:
            log_audit(f"自主停止，原因: {reason}")
            break
    
    # 筛选最终最优方案
    final_solution = select_final_solution(memory_base.all_records(), mode=target_mode)
    return final_solution |
| --- |


---

## 附录：核心符号对照表

| 符号 | 含义 | 锁档值 |
|------|------|------|
| γ | 时序衰减系数 | 0.92 |
| κ | 虚实阻尼系数 | 0.35 |
| α | 稀疏补偿系数 | 0.18 |
| E₁ | 一阶肉身能级阈值 | 0.35 |
| E₂ | 二阶精神能级阈值 | 0.65 |
| E₃ | 三阶道心能级阈值 | 0.90 |
| θ_mv | 科研边际价值判定阈值 | 0.005 |
| θ_evo | 自进化增量阈值 | 0.002 |
| θ_neg | 负迁移判定阈值 | 0.02 |

---

