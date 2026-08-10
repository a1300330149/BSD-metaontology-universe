
---
向量标签
---

# 基底层级标签
base_0:元道本源基底

# 公理标签
axiom_1:宿命双边界公理, axiom_2:自主科研闭环动力学公理, axiom_3:科研价值边际判定公理, axiom_4:选题创化生成机制, axiom_5:成果落地转化范式, axiom_7:系统自进化迭代公理

# 九维维度标签
因果社会, 天道原理, 天道动力学

# 参数标签
- gamma: 0.92
- kappa: 0.35
- alpha: 0.18
- E1: 0.35
- E2: 0.65
- E3: 0.9

# 关键词标签
元本体, 公理, 宿命, 舒适, 自然, 科研, 能级

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

二阶分布纠偏系统（SOD-DBS）工程化完整设计文档

阶段 2 二阶分布纠偏系统（Second-Order Distribution Debiasing System, SOD-DBS）

工程化完整设计文档（承接阶段 1 FO-EFS，可直接交付代码落地）

阶段定位：整套自动科研系统的「精神纠偏层」，对应二阶精神觉醒阶段。在一阶实体拟合能力的基础上，系统性解决一阶模型天然存在的分布偏置、幻相失真、精度 - 多样性对冲等固有缺陷，实现「拟合精度 + 分布均衡 + 泛化稳定」多目标平衡，是系统从 “能跑通” 升级为 “效果稳、无偏置、泛化强” 的核心跃迁，也是后续三阶智能决策的重要能力底座。

理论溯源：虚实二分理论、模态分划本体、舒适边界公理、二阶精神觉醒理论、六系相变自然层 + 创化社会层动力学、流行度幻相偏置校正原理。

前置依赖：阶段 0 OCE 元本体核心引擎、阶段 1 FO-EFS 一阶实体拟合系统均已完成开发并通过验收；二阶系统以插件化方式叠加在一阶系统之上，不修改一阶内核逻辑，仅通过标准 API 调用一阶能力。



一、全局架构与接口规范

1. 模块层级关系

2. 命名空间规范

根包名：sod_dbs

所有模块通过 sod_dbs.adapter 调用一阶系统能力与内核能力，禁止直接跨层调用

所有去偏策略、融合方案、多目标权重均标记为「主观幻相」，需经实相验证后才能生效

所有偏置量化指标、去偏后真实效果均标记为「实体实相」，开启写保护

3. 全局枚举定义



二、模块一：一阶系统适配层（SOD Adapter）

理论溯源

对应「模态分划本体的层间交互规则」，二阶系统作为上层能力，通过标准化适配层对接一阶实体系统，保证层间解耦、能力复用、边界一致。

核心职责

封装一阶系统所有对外 API，提供偏置检测、去偏训练、融合推理的业务化接口

统一透传 OCE 内核校验：所有去偏实验均经过宿命边界、舒适边界双重校验

统一数据分类标记：偏置指标标记为实相，去偏策略标记为幻相，自动完成虚实校准

透传审计日志，保证去偏全流程可追溯、可复现

核心函数伪代码

1. 带偏置检测的实验执行入口



三、模块二：偏置检测引擎（Bias Detection Engine）

理论溯源

对应「虚实二分理论的幻相偏差量化」，主动识别一阶模型输出中的分布偏置、预测坍缩、泛化偏差等幻相失真问题，是去偏的前提 —— 先精准诊断，再针对性治疗。

核心职责

自动识别任务类型对应的所有潜在偏置类型，量化偏置程度

输出结构化偏置报告，包含偏置类型、严重程度、影响范围、根因分析

支持单维度偏置检测与全维度偏置扫描

检测结果标记为实体实相，作为去偏策略匹配的唯一依据

核心数据结构

核心函数伪代码

1. 全量偏置扫描



四、模块三：通用去偏算法库（Debiasing Algorithm Zoo）

理论溯源

对应「虚实二分的幻相校正机制」，通过损失加权、重采样、长尾增强、融合校正等方式，修正模型的分布偏置，让幻相预测更贴近实相分布。

核心职责

按偏置类型分类管理去偏算法，提供标准化调用接口

支持算法组合使用，叠加多重去偏效果

内置赛题双任务专属去偏算法，直接对应已验证的优化方案

可扩展新的去偏算法，只需适配统一接口

内置去偏算法清单

核心函数伪代码

1. 去偏策略应用器



五、模块四：多目标平衡调度器（Multi-Objective Balance Scheduler）

理论溯源

对应「舒适边界公理的多维度稳态」，打破单目标优化的局限，在精度、多样性、公平性、效率等多个目标间寻找帕累托最优，让系统运行在多维舒适区间内，避免单目标优化导致的其他维度坍缩。

核心职责

支持多目标权重配置，可按任务需求调整各维度优先级

实现多目标帕累托寻优，输出均衡最优解

动态校验多维度舒适边界，超出区间自动调整优化方向

提供多目标结果评估与排序，筛选最终最优方案

核心数据结构

核心函数伪代码

1. 帕累托最优筛选

2. 舒适边界多目标校验



六、模块五：分层融合引擎（Hierarchical Fusion Engine）

理论溯源

对应「虚实二分 + 阶位互补的校正机制」，利用低阶统计模型的分布均衡性，校正高阶深度模型的偏置坍缩，实现精度与多样性的优势互补，是解决 “精度 - 多样性对冲” 的核心模块。

核心职责

支持多阶位、多模型的标准化融合，统一融合接口

内置分层插槽融合算法，精准控制精度与多样性的平衡比例

支持融合权重自动寻优，匹配不同任务的最优融合比例

融合结果自动完成虚实校准，保证效果可追溯

核心函数伪代码

1. 分层插槽融合（推荐任务专属，已验证最优方案）

2. 分类任务概率融合



七、模块六：偏差校准与经验沉淀模块

理论溯源

对应「因果社会系的经验沉淀机制」，记录每一次偏置检测、去偏策略、效果提升的完整轨迹，沉淀为可复用的去偏经验，为三阶智能 Agent 提供决策依据。

核心职责

结构化存储所有去偏实验的完整链路数据

统计不同偏置类型对应最优去偏策略与效果增益

提供相似偏置场景的经验检索，加速后续实验决策

自动更新去偏策略匹配优先级，持续优化去偏准确率

核心函数伪代码



八、阶段 2 对外统一 API



九、阶段 2 落地验收标准

完成代码开发后，满足以下全部条件即视为阶段 2 验收通过，可进入三阶系统开发：

偏置检测验证：可自动识别分类任务类别不平衡、预测坍缩，推荐任务流行度偏置、冷启动偏置，输出量化严重程度，准确率≥95%

去偏效果验证：

分类任务：针对初始 0.37 准确率的单类坍缩场景，去偏后准确率稳定提升至 0.7+，少数类召回率提升≥50%

推荐任务：针对多样性 315 / 万人的流行度偏置场景，去偏 + 融合后多样性提升至 3000+/ 万人，召回率损失≤2%

多目标优化验证：可输出帕累托最优解集，支持精度、多样性双目标权衡，可按权重筛选最优方案

分层融合验证：内置分层插槽融合算法可直接运行，融合结果格式合规，指标符合预期

边界合规验证：所有去偏实验均经过内核边界校验，无超预算、并行违规问题

经验沉淀验证：去偏实验可自动沉淀经验，支持相似场景检索复用

赛题场景验证：针对赛题双任务，一键执行即可完成 “基线训练→偏置检测→自动去偏→融合输出→生成提交文件” 全流程



下一步推进说明

阶段 2 完成后，系统已具备完整的偏置识别、去偏校正、多目标平衡、分层融合能力，彻底解决一阶模型的精度 - 多样性对冲、分布偏置、预测坍缩等核心问题，赛题双任务指标可达到中上游水平。后续将进入阶段 3（三阶智能决策系统），搭建完整的实验记忆、智能寻优、复盘反思、自主停止的 Agent 闭环，实现真正意义上的全自动科研迭代。

|（注：部分内容可能由 AI 生成）

| Plain Text
┌───────────────────────────────────────────────────┐
│ 二阶分布纠偏系统 SOD-DBS                          │
│  ┌──────────┬──────────┬──────────┬──────────┐   │
│  │ 偏置检测 │ 去偏算法 │ 多目标   │ 分层融合 │   │
│  │ 引擎     │ 库       │ 调度器   │ 引擎     │   │
│  └──────────┴──────────┴──────────┴──────────┘   │
│              二阶系统适配层                        │
└───────────────────────────────────────────────────┘
        ↓ 统一调用一阶API
┌───────────────────────────────────────────────────┐
│ 一阶实体拟合系统 FO-EFS                            │
└───────────────────────────────────────────────────┘
        ↓ 统一调用OCE API
┌───────────────────────────────────────────────────┐
│ 阶段0 元本体核心引擎 OCE                          │
└───────────────────────────────────────────────────┘ |
| --- |

| python
from enum import Enum

class BiasType(Enum):
    """可识别的偏置类型，可扩展"""
    CLASS_IMBALANCE = "class_imbalance"          # 类别分布不平衡（分类任务）
    POPULARITY_BIAS = "popularity_bias"          # 流行度偏置（推荐任务）
    PREDICTION_COLLAPSE = "prediction_collapse"  # 预测坍缩（全输出同一类别/热门物品）
    OVERFIT_BIAS = "overfit_bias"                # 过拟合偏置（泛化性差）
    SPARSE_BIAS = "sparse_bias"                  # 稀疏样本偏置（冷启动/低度节点效果差）

class DebiasStrategy(Enum):
    """去偏策略枚举"""
    LOSS_WEIGHT = "loss_weight"        # 损失加权
    RESAMPLING = "resampling"          # 重采样
    ADVERSARIAL = "adversarial"        # 对抗去偏
    FUSION_CORRECT = "fusion_correct"  # 融合校正
    LONGTAIL_ENHANCE = "longtail_enhance" # 长尾增强

class MultiObjectiveTarget(Enum):
    """多目标优化维度"""
    ACCURACY = "accuracy"      # 精度（准确率/召回率）
    DIVERSITY = "diversity"    # 多样性（覆盖度/基尼系数）
    FAIRNESS = "fairness"      # 公平性（少数类/冷启动效果）
    GENERALIZATION = "generalization" # 泛化性（验证集与测试集偏差）
    EFFICIENCY = "efficiency"  # 效率（训练耗时/算力消耗） |
| --- |

| python
def run_debiased_experiment(dataset, model_name, hyper_params, debias_config=None) -> ExperimentResult:
    """
    二阶去偏实验统一入口
    1. 前置边界校验 2. 运行一阶基线实验 3. 偏置检测 4. 匹配去偏策略 5. 重训练输出结果
    """
    # 宿命边界前置校验
    passed, msg = oce_adapter.hard_check({"budget_used": get_budget_used()})
    if not passed:
        return ExperimentResult(status=TrainStatus.BLOCKED_BY_BOUNDARY)
    
    # 先跑一阶基线，获取基准结果
    base_result = fo_efs_api.run_single_experiment(dataset, model_name, hyper_params)
    
    # 偏置检测
    bias_report = bias_detector.detect(base_result, dataset)
    
    # 匹配去偏策略并执行重训练
    if debias_config is None:
        debias_config = debias_strategy_matcher.match(bias_report)
    
    debiased_params = apply_debias_to_params(hyper_params, debias_config)
    debiased_result = fo_efs_api.run_single_experiment(dataset, model_name, debiased_params)
    
    # 记录去偏效果
    debiased_result.debias_info = {
        "bias_report": bias_report,
        "strategy": debias_config,
        "improvement": calc_improvement(base_result, debiased_result)
    }
    
    return debiased_result |
| --- |

| python
class BiasReport:
    task_type: TaskType
    has_bias: bool
    bias_items: list[BiasItem]
    overall_severity: float  # 0~1，整体偏置严重程度

class BiasItem:
    bias_type: BiasType
    severity: float         # 0~1，单类偏置严重程度
    affected_ratio: float   # 受影响样本占比
    root_cause: str         # 根因分析
    suggest_strategy: list[DebiasStrategy] # 建议去偏策略 |
| --- |

| python
def detect_full(result: ExperimentResult, dataset: StandardDataset) -> BiasReport:
    """全维度偏置扫描，输出完整偏置报告"""
    bias_items = []
    
    # 1. 分类任务：类别不平衡+预测坍缩检测
    if dataset.task_type == TaskType.GRAPH_NODE_CLASSIFY:
        # 检测训练集类别分布不平衡
        imb_ratio = calc_class_imbalance_ratio(dataset.train_data.labels)
        if imb_ratio > 3.0:
            bias_items.append(BiasItem(
                bias_type = BiasType.CLASS_IMBALANCE,
                severity = min(1.0, imb_ratio / 10.0),
                affected_ratio = calc_minority_ratio(dataset.train_data.labels),
                root_cause = "训练集类别分布差异过大，多数类主导梯度",
                suggest_strategy = [DebiasStrategy.LOSS_WEIGHT, DebiasStrategy.RESAMPLING]
            ))
        
        # 检测预测坍缩（单类别占比过高）
        collapse_ratio = calc_max_pred_ratio(result.pred_result.content)
        if collapse_ratio > 0.5:
            bias_items.append(BiasItem(
                bias_type = BiasType.PREDICTION_COLLAPSE,
                severity = collapse_ratio,
                affected_ratio = 1.0,
                root_cause = "模型欠拟合+分布不平衡，退化为全局均值预测",
                suggest_strategy = [DebiasStrategy.LOSS_WEIGHT, DebiasStrategy.FUSION_CORRECT]
            ))
    
    # 2. 推荐任务：流行度偏置+稀疏冷启动偏置检测
    elif dataset.task_type == TaskType.GRAPH_LINK_PREDICT:
        # 检测流行度偏置（推荐结果集中于热门物品）
        pop_gini = calc_popularity_gini(result.pred_result.content)
        if pop_gini > 0.7:
            bias_items.append(BiasItem(
                bias_type = BiasType.POPULARITY_BIAS,
                severity = pop_gini,
                affected_ratio = calc_hot_item_ratio(result.pred_result.content),
                root_cause = "深度模型过度学习热门模式，长尾物品被压制",
                suggest_strategy = [DebiasStrategy.LONGTAIL_ENHANCE, DebiasStrategy.FUSION_CORRECT]
            ))
        
        # 检测冷启动稀疏偏置
        cold_start_gap = calc_cold_start_performance_gap(result, dataset)
        if cold_start_gap > 0.3:
            bias_items.append(BiasItem(
                bias_type = BiasType.SPARSE_BIAS,
                severity = cold_start_gap,
                affected_ratio = calc_cold_user_ratio(dataset),
                root_cause = "稀疏用户交互不足，模型无法学习有效表征",
                suggest_strategy = [DebiasStrategy.FUSION_CORRECT, DebiasStrategy.LONGTAIL_ENHANCE]
            ))
    
    # 3. 通用：过拟合偏置检测
    gen_gap = calc_train_val_gap(result)
    if gen_gap > 0.2:
        bias_items.append(BiasItem(
            bias_type = BiasType.OVERFIT_BIAS,
            severity = gen_gap,
            affected_ratio = 1.0,
            root_cause = "模型容量过大或训练过度，泛化性差",
            suggest_strategy = [DebiasStrategy.LOSS_WEIGHT]
        ))
    
    overall_severity = max([item.severity for item in bias_items]) if bias_items else 0.0
    return BiasReport(
        task_type = dataset.task_type,
        has_bias = len(bias_items) > 0,
        bias_items = bias_items,
        overall_severity = overall_severity
    ) |
| --- |

| 算法名称 | 适配偏置类型 | 对应任务 | 核心原理 |
| --- | --- | --- | --- |
| 加权交叉熵损失 | 类别不平衡、预测坍缩 | 分类任务 | 少数类损失加权，平衡梯度 |
| 分层重采样 | 类别不平衡 | 分类任务 | 少数类过采样、多数类欠采样 |
| 去偏 BPR 损失 | 流行度偏置 | 推荐任务 | 长尾物品损失加权，抑制热门偏好 |
| 长尾负采样 | 流行度偏置、稀疏偏置 | 推荐任务 | 增加长尾负样本，提升区分度 |
| 特征增强 | 稀疏偏置、冷启动 | 双任务 | 稀疏样本补充特征信息 |
| 标签平滑 | 过拟合偏置 | 双任务 | 抑制模型过度自信，提升泛化 |
| 高低阶融合校正 | 全类型偏置 | 双任务 | 统计模型补全深度模型偏置 |

| python
def apply_debias_strategy(model_config: dict, dataset: StandardDataset, 
                          bias_report: BiasReport) -> dict:
    """
    根据偏置报告自动匹配并应用去偏策略，返回修正后的模型配置
    """
    debiased_config = model_config.copy()
    
    for bias_item in bias_report.bias_items:
        for strategy in bias_item.suggest_strategy:
            if strategy == DebiasStrategy.LOSS_WEIGHT:
                debiased_config["class_weights"] = calc_class_weights(dataset.train_data)
                debiased_config["label_smoothing"] = 0.1
            elif strategy == DebiasStrategy.RESAMPLING:
                debiased_config["enable_resample"] = True
                debiased_config["resample_ratio"] = 0.5
            elif strategy == DebiasStrategy.LONGTAIL_ENHANCE:
                debiased_config["pop_debias_weight"] = 0.3
                debiased_config["longtail_neg_ratio"] = 0.3
            elif strategy == DebiasStrategy.FUSION_CORRECT:
                debiased_config["enable_fusion"] = True
                debiased_config["fusion_alpha"] = 0.7
    
    return debiased_config |
| --- |

| python
class MultiObjectiveConfig:
    targets: dict[MultiObjectiveTarget, float]  # 目标与对应权重
    constraints: dict[MultiObjectiveTarget, float] # 目标最低约束阈值
    optimize_direction: dict[MultiObjectiveTarget, str] # maximize/minimize

class ParetoSolution:
    solution_id: str
    hyper_params: dict
    scores: dict[MultiObjectiveTarget, float]
    is_pareto_optimal: bool |
| --- |

| python
def filter_pareto_front(solutions: list[ParetoSolution], 
                        mo_config: MultiObjectiveConfig) -> list[ParetoSolution]:
    """筛选帕累托最优解集，所有解均无法在不损失其他目标的前提下提升单一目标"""
    pareto_set = []
    for sol in solutions:
        dominated = False
        for other in solutions:
            # 判断other是否支配sol（所有目标都不差，至少一个目标更优）
            all_better = True
            any_better = False
            for target, direction in mo_config.optimize_direction.items():
                if direction == "maximize":
                    if other.scores[target] < sol.scores[target]:
                        all_better = False
                    elif other.scores[target] > sol.scores[target]:
                        any_better = True
                else:
                    if other.scores[target] > sol.scores[target]:
                        all_better = False
                    elif other.scores[target] < sol.scores[target]:
                        any_better = True
            if all_better and any_better:
                dominated = True
                break
        if not dominated:
            sol.is_pareto_optimal = True
            pareto_set.append(sol)
    return pareto_set |
| --- |

| python
def check_multi_objective_comfort(scores: dict, mo_config: MultiObjectiveConfig) -> tuple[bool, list]:
    """校验多目标是否均满足舒适区间约束，返回是否合规与不达标项"""
    failed_targets = []
    for target, min_threshold in mo_config.constraints.items():
        if scores.get(target, 0) < min_threshold:
            failed_targets.append(target)
    return len(failed_targets) == 0, failed_targets |
| --- |

| python
def slot_fusion_predict(high_score: np.ndarray, low_score: np.ndarray, 
                        item_popularity: np.ndarray, interacted: set,
                        precision_slot=3, balance_slot=4, diversity_slot=3,
                        alpha=0.68, pop_penalty=0.35) -> list[int]:
    """
    分层插槽融合：头部高精度、中部平衡、尾部补多样性
    high_score: 高阶深度模型得分（三阶LightGCN）
    low_score: 低阶统计模型得分（二阶ItemCF）
    """
    # 屏蔽已交互物品
    high_score = high_score.copy()
    low_score = low_score.copy()
    for i in interacted:
        high_score[i] = -1e9
        low_score[i] = -1e9
    
    # 归一化
    def norm(x):
        min_s, max_s = x.min(), x.max()
        if max_s - min_s < 1e-6:
            return np.zeros_like(x)
        return (x - min_s) / (max_s - min_s)
    
    high_norm = norm(high_score)
    low_norm = norm(low_score)
    pop_norm = 1.0 - norm(item_popularity)
    
    # 头部精准插槽：纯高阶结果
    high_sort = np.argsort(-high_norm)
    precise_items = []
    for idx in high_sort:
        if idx not in interacted:
            precise_items.append(idx)
        if len(precise_items) >= precision_slot:
            break
    used = set(precise_items)
    
    # 中部平衡插槽：双模型融合+流行度惩罚
    mid_pool = list(set(high_sort[:50]) | set(np.argsort(-low_norm)[:50]) - used)
    mid_score = alpha * high_norm[mid_pool] + (1-alpha) * low_norm[mid_pool] + pop_penalty * pop_norm[mid_pool]
    mid_items = [mid_pool[i] for i in np.argsort(-mid_score)[:balance_slot]]
    used.update(mid_items)
    
    # 尾部多样性插槽：低阶长尾优先
    tail_pool = [x for x in np.argsort(-low_norm) if x not in used]
    tail_score = low_norm[tail_pool] + 0.5 * pop_norm[tail_pool]
    tail_items = [tail_pool[i] for i in np.argsort(-tail_score)[:diversity_slot]]
    
    final = precise_items + mid_items + tail_items
    return final[:10] |
| --- |

| python
def classify_prob_fusion(high_pred: np.ndarray, low_pred: np.ndarray, alpha=0.7) -> np.ndarray:
    """分类任务概率加权融合，平衡精度与分布均衡性"""
    fused = alpha * high_pred + (1 - alpha) * low_pred
    return np.argmax(fused, axis=1) |
| --- |

| python
def record_debias_experiment(exp_id: str, bias_report: BiasReport, 
                             strategy: list, result: ExperimentResult):
    """沉淀去偏实验经验"""
    record = {
        "exp_id": exp_id,
        "task_type": bias_report.task_type,
        "bias_types": [item.bias_type.value for item in bias_report.bias_items],
        "severity": bias_report.overall_severity,
        "strategy": strategy,
        "improvement": result.val_metrics["score"] - base_score,
        "diversity_change": diversity_delta
    }
    _debias_experience_pool.append(record)

def retrieve_similar_experience(bias_report: BiasReport) -> list:
    """检索相似偏置场景的历史最优经验"""
    similar = []
    for record in _debias_experience_pool:
        if set(record["bias_types"]) & set([i.bias_type.value for i in bias_report.bias_items]):
            similar.append(record)
    # 按效果增益排序
    similar.sort(key=lambda x: x["improvement"], reverse=True)
    return similar[:5] |
| --- |

| python
# sod_dbs/api.py 对外暴露
from .bias_detector import detect_full, BiasReport
from .debias_zoo import apply_debias_strategy, list_debias_algorithms
from .multi_objective import filter_pareto_front, MultiObjectiveConfig
from .fusion_engine import slot_fusion_predict, classify_prob_fusion
from .pipeline import run_debiased_experiment, run_multi_objective_search
from .types import BiasType, DebiasStrategy, MultiObjectiveTarget |
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

---
> **BSD跨层耦合引用** (卫星系统→行星轨道):
> [T88 BSD全域经济元体系——修正传统经济学核心盲区·嵌入智能文明供需新范式](./作者猜想/T88 BSD全域经济元体系——修正传统经济学核心盲区·嵌入智能文明供需新范式.md) (跨层耦合: 卫星系统↔行星轨道)
> [BSD终极终审——Π₂定义·不可说命题·范式革新与八维自证完整论证合集](./0元本体论大一统/BSD终极终审——Π₂定义·不可说命题·范式革新与八维自证完整论证合集.md) (跨层耦合: 卫星系统↔行星轨道)
