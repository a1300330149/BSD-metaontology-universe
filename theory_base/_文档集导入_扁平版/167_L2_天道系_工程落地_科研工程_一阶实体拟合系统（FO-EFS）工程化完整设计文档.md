
---
向量标签
---

# 基底层级标签
base_0:元道本源基底

# 公理标签
axiom_1:宿命双边界公理, axiom_3:科研价值边际判定公理, axiom_5:成果落地转化范式, axiom_7:系统自进化迭代公理

# 九维维度标签
载体实体

# 参数标签
- gamma: 0.92
- kappa: 0.35
- alpha: 0.18
- E1: 0.35
- E2: 0.65
- E3: 0.9

# 关键词标签
元本体, 双边界, 公理, 宿命, 舒适, 科研, 能级

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

一阶实体拟合系统（FO-EFS）工程化完整设计文档

阶段 1 一阶实体拟合系统（First-Order Entity Fitting System, FO-EFS）

工程化完整设计文档（承接阶段 0 OCE 内核，可直接交付代码落地）

阶段定位：整套自动科研系统的「肉身载体层」，对应一阶肉身蜕变阶段。基于阶段 0 元本体核心引擎（OCE）的底层约束，实现标准化的数据接入、模型实体管理、自动化训练验证、基础超参搜索，完成单任务端到端的自动化拟合能力，是后续高阶智能、跨域泛化能力的实体底座。

理论溯源：实体原本体、一阶肉身蜕变理论、物理四层级拓扑实体层、六系载体实体系、宿命 / 舒适双边界公理。

前置依赖：阶段 0 OCE 内核已完成开发并通过验收，所有上层操作必须通过 OCE API 执行校验，禁止绕过内核直接操作。



一、全局架构与接口规范

1. 模块层级关系

2. 命名空间规范

根包名：fo_efs

所有模块必须通过 fo_efs.adapter 调用 OCE 内核能力，禁止直接导入 OCE 内部实现

所有实体数据（数据集、训练好的模型、验证真值）自动由适配层标记为「实体实相」，开启写保护

所有预测、预估结果自动标记为「主观幻相」，需经实相校准

3. 全局状态枚举



二、模块一：内核适配层（OCE Adapter）

理论溯源

对应「实体层与元模态层的交互接口」，是所有上层业务接入内核的唯一网关，保障所有操作都受宿命边界约束、所有数据都有本体层级标记，杜绝越权操作。

核心职责

封装 OCE 所有对外 API，提供业务友好的调用方式，上层无需感知内核细节

统一执行宿命边界前置校验：所有实验启动前必须校验预算、并行数、合规性

统一执行数据本体分类：自动标记实相 / 幻相数据，开启实相写保护

统一执行舒适边界软调度：训练过程中检测状态，自动给出修正建议

统一记录审计日志：所有操作全链路留痕，可追溯、可复现

核心函数伪代码

1. 实验启动前置校验（必调）

2. 数据自动分类标记

3. 训练过程舒适区检测



三、模块二：标准化数据集加载器（Standard Dataset Loader）

理论溯源

对应「实体原本体的数据载体属性」，所有科研数据都是客观实相，必须标准化接入、只读保护、可追溯，是模型拟合的唯一真值来源。

核心职责

支持多类型科研数据的统一加载与格式标准化

自动完成数据校验、清洗、划分、预处理

加载后自动标记为「实体实相」，开启写保护，禁止训练中修改原始数据

数据集版本化管理，所有实验可追溯对应的数据版本

内置赛题双任务数据解析能力（CSR 图数据、推荐二部图数据）

核心数据结构

核心函数伪代码

1. 通用数据加载入口

2. 内置赛题分类任务解析（CSR 格式）

3. 内置赛题推荐任务解析（二部图序列数据）



四、模块三：模型实体库（Model Entity Zoo）

理论溯源

对应「一阶肉身的载体形态」，不同模型是不同能力的肉身载体，统一接口规范，可插拔替换，随阶位提升逐步升级。

核心职责

按任务领域分类管理基线模型，提供统一调用接口

所有模型实现标准化的训练、预测、保存、加载方法

内置一阶基线模型，覆盖赛题双任务

支持扩展新模型，只需适配统一接口，无需修改流水线

模型实体自动标记为「实体实相」，权重文件可追溯、可复现

核心数据结构

内置一阶基线模型

核心函数伪代码

1. 模型工厂实例化



五、模块四：自动化训练流水线（Auto Training Pipeline）

理论溯源

对应「实体层的演化拟合过程」，模型通过训练数据完成参数拟合，对应肉身载体的能力成型过程，全程受双边界约束。

核心职责

标准化执行「数据加载→模型初始化→训练→验证→早停→结果保存」全流程

全程对接 OCE 内核：前置校验宿命边界、过程检测舒适边界、结果自动分类标记

内置早停机制、学习率调度、指标记录，保证训练稳定可复现

自动记录实验全量元数据，支持溯源复现

串行单任务执行，严格符合「禁止并行」的宿命边界规则

核心数据结构

核心函数伪代码

1. 单轮实验全流程执行



六、模块五：基础超参搜索器（Basic Hyperparameter Searcher）

理论溯源

对应「一阶肉身的基础探索能力」，通过网格搜索、随机搜索遍历基础参数空间，为后续高阶智能寻优提供初始经验数据，是从手动调参到自动寻优的过渡。

核心职责

支持网格搜索、随机搜索两种基础寻优策略

自动生成超参组合，串行调用训练流水线执行实验

自动记录所有实验结果，输出最优配置

严格串行执行，符合禁止并行规则

输出的实验结果自动沉淀，为三阶智能 Agent 提供初始记忆库

核心函数伪代码

1. 网格搜索执行

2. 随机搜索执行



七、阶段 1 对外统一 API



八、阶段 1 落地验收标准

完成代码开发后，满足以下全部条件即视为阶段 1 验收通过，可进入二阶系统开发：

数据加载与写保护验证：可正确加载赛题双任务数据集；尝试修改原始数据，触发实相写保护拦截，修改失败

基线训练验证：单轮实验可自动完成 GAT 分类、LightGCN 推荐的全流程训练，输出验证指标，结果可复现

宿命边界验证：预算耗尽后启动新实验，自动被拦截，返回 BLOCKED_BY_BOUNDARY 状态

舒适边界验证：训练波动过大时，自动触发软调度提示，可输出修正建议

基础寻优验证：网格搜索可遍历超参组合，自动输出最优配置；全程串行执行，无并行违规

虚实校准验证：预测结果自动标记为幻相，可通过验证集真值校准，生成 delta_illu 偏差值

全链路溯源验证：任意实验可追溯对应数据集版本、模型配置、超参数、训练日志，100% 可复现

赛题提交生成验证：可基于训练好的模型自动生成符合赛题格式的 A1.csv、A2.csv，格式校验 100% 通过



下一步推进说明

阶段 1 完成后，系统已具备单任务自动化拟合与基础寻优能力，可独立完成赛题双任务的基线训练与结果输出。后续将进入阶段 2（二阶分布纠偏系统），在一阶拟合能力基础上，叠加去偏、多目标平衡、分层融合能力，解决精度与多样性的对冲问题。

|（注：部分内容可能由 AI 生成）

| Plain Text
┌─────────────────────────────────────────┐
│ 一阶实体拟合系统 FO-EFS                  │
│  ┌─────────┬─────────┬──────────────┐  │
│  │ 数据集  │ 模型库  │ 训练流水线   │  │
│  │ 加载器  │         │ 基础寻优器   │  │
│  └─────────┴─────────┴──────────────┘  │
│              内核适配层                 │
└─────────────────────────────────────────┘
        ↓ 统一调用OCE API
┌─────────────────────────────────────────┐
│ 阶段0 元本体核心引擎 OCE                │
└─────────────────────────────────────────┘ |
| --- |

| python
from enum import Enum

class TaskType(Enum):
    """支持的科研任务类型，可扩展"""
    GRAPH_NODE_CLASSIFY = "graph_node_classify"    # 图节点分类（赛题分类任务）
    GRAPH_LINK_PREDICT = "graph_link_predict"      # 图链接预测（赛题推荐任务）
    TABULAR_CLASSIFY = "tabular_classify"
    SEQUENCE_PREDICT = "sequence_predict"

class TrainStatus(Enum):
    INIT = "init"
    TRAINING = "training"
    VALIDATING = "validating"
    FINISHED = "finished"
    STOPPED_EARLY = "stopped_early"
    BLOCKED_BY_BOUNDARY = "blocked_by_boundary" |
| --- |

| python
def before_experiment_check(exp_config: dict) -> tuple[bool, str]:
    """
    实验启动前统一校验，触发宿命边界则直接拦截
    校验项：预算剩余、并行数量、数据合规、格式规范
    """
    fact = {
        "budget_used": exp_config["budget_used"],
        "parallel_count": 1,  # 一阶默认串行，符合禁止并行规则
        "dataset_source": exp_config["dataset_source"]
    }
    passed, msg = oce.api.hard_check(fact)
    if not passed:
        log_audit(f"实验被宿命边界拦截: {msg}")
        return False, msg
    return True, "校验通过" |
| --- |

| python
def mark_data(data: any, source_type: str) -> ClassifiedData:
    """
    自动调用OCE分类器标记数据层级
    实相数据自动开启写保护，幻相数据记录初始置信度
    """
    classified = oce.api.classify_data(data, source_type)
    if classified.layer == OntologyLayer.ENTITY_REAL:
        log_audit(f"实相数据已标记，开启写保护: {source_type}")
    return classified |
| --- |

| python
def train_comfort_check(train_state: dict) -> dict:
    """训练中定期检测舒适边界，返回修正建议"""
    in_comfort, msg, suggestions = oce.api.soft_check(train_state)
    if not in_comfort:
        log_audit(f"超出舒适边界: {msg}, 建议调整: {suggestions}")
    return suggestions |
| --- |

| python
class StandardDataset:
    dataset_id: str
    task_type: TaskType
    raw_data: ClassifiedData  # 原始数据，实相标记，只读
    train_data: any
    val_data: any
    test_data: any
    meta_info: dict           # 数据规模、特征维度、类别数等元信息
    version: str |
| --- |

| python
def load_dataset(dataset_path: str, task_type: TaskType, val_ratio: float = 0.2) -> StandardDataset:
    """
    统一数据加载入口，根据任务类型调用对应解析器
    加载完成后自动标记实相、开启写保护
    """
    # 按任务类型解析原始数据
    if task_type == TaskType.GRAPH_NODE_CLASSIFY:
        raw_data, meta = _load_graph_classification(dataset_path)
    elif task_type == TaskType.GRAPH_LINK_PREDICT:
        raw_data, meta = _load_link_prediction(dataset_path)
    else:
        raise ValueError(f"暂不支持的任务类型: {task_type}")
    
    # 自动标记为实体实相，开启写保护
    classified_raw = adapter.mark_data(raw_data, "official_dataset")
    
    # 分层划分验证集
    train, val = _split_train_val(classified_raw.content, val_ratio, task_type)
    
    dataset = StandardDataset(
        dataset_id = generate_id(),
        task_type = task_type,
        raw_data = classified_raw,
        train_data = train,
        val_data = val,
        test_data = None,
        meta_info = meta,
        version = "v1.0"
    )
    log_audit(f"数据集加载完成: {dataset_id}, 已标记实相只读")
    return dataset |
| --- |

| python
def _load_graph_classification(npz_path: str) -> tuple[dict, dict]:
    """解析官方.npz格式的图节点分类数据"""
    data = np.load(npz_path)
    adj = csr_matrix(
        (data["adj_data"], data["adj_indices"], data["adj_indptr"]),
        shape=data["adj_shape"]
    )
    x = csr_matrix(
        (data["attr_data"], data["attr_indices"], data["attr_indptr"]),
        shape=data["attr_shape"]
    ).todense()
    labels = data["labels"]
    train_idx = data["train_idx"]
    test_idx = data["test_idx"]
    
    meta = {
        "node_count": data["adj_shape"][0],
        "feature_dim": data["attr_shape"][1],
        "class_num": len(np.unique(labels[train_idx])),
        "train_node_num": len(train_idx),
        "test_node_num": len(test_idx)
    }
    return {
        "adj": adj, "x": x, "labels": labels,
        "train_idx": train_idx, "test_idx": test_idx
    }, meta |
| --- |

| python
def _load_link_prediction(data_dir: str) -> tuple[dict, dict]:
    """解析推荐任务的用户-物品二部图与交互序列数据"""
    train_df = pd.read_csv(f"{data_dir}/train.csv")
    test_df = pd.read_csv(f"{data_dir}/test.csv")
    user_df = pd.read_csv(f"{data_dir}/user.csv")
    item_df = pd.read_csv(f"{data_dir}/item.csv")
    
    # ID映射、交互对构建、特征提取
    uid2idx, iid2idx, train_pairs, user_interacted = _build_interaction_graph(train_df)
    meta = {
        "user_num": len(uid2idx),
        "item_num": len(iid2idx),
        "train_user_num": len(train_df),
        "test_user_num": len(test_df)
    }
    return {
        "train_pairs": train_pairs,
        "user_interacted": user_interacted,
        "user_feat": user_df,
        "item_feat": item_df,
        "test_uids": test_df["uid"].tolist(),
        "uid2idx": uid2idx,
        "iid2idx": iid2idx
    }, meta |
| --- |

| python
class BaseModel(ABC):
    """所有模型必须继承的抽象基类，统一接口规范"""
    model_id: str
    task_type: TaskType
    config: dict
    is_trained: bool

    @abstractmethod
    def train(self, train_data, val_data, config: dict) -> dict:
        """执行训练，返回训练指标"""
        pass

    @abstractmethod
    def predict(self, test_data) -> np.ndarray:
        """执行预测，返回预测结果"""
        pass

    @abstractmethod
    def save(self, save_path: str) -> None:
        """保存模型权重"""
        pass

    @abstractmethod
    def load(self, load_path: str) -> None:
        """加载模型权重"""
        pass |
| --- |

| 模型名称 | 对应任务 | 定位 |
| --- | --- | --- |
| GATClassifier | 图节点分类 | 一阶分类基线，解决欠拟合与类别坍缩 |
| LightGCNRec | 图链接预测 / 推荐 | 一阶推荐基线，基础协同过滤 + 图卷积 |
| MLPClassifier | 通用分类 | 最简基线，快速跑通 |
| ItemCF | 推荐任务 | 二阶统计基线，补充多样性 |

| python
def create_model(model_name: str, task_type: TaskType, model_config: dict) -> BaseModel:
    """模型工厂，根据名称创建对应模型实例"""
    model_map = {
        "GATClassifier": GATClassifier,
        "LightGCNRec": LightGCNRec,
        "MLPClassifier": MLPClassifier,
        "ItemCF": ItemCF
    }
    if model_name not in model_map:
        raise ValueError(f"未收录的模型: {model_name}")
    model = model_map[model_name](task_type=task_type, config=model_config)
    log_audit(f"模型实例化完成: {model_name}")
    return model |
| --- |

| python
class ExperimentResult:
    exp_id: str
    model_name: str
    dataset_id: str
    hyper_params: dict
    train_metrics: dict
    val_metrics: dict       # 验证集真实指标，实相标记
    pred_result: ClassifiedData  # 预测结果，幻相标记
    train_status: TrainStatus
    cost_budget: int        # 消耗预算轮次
    timestamp: str |
| --- |

| python
def run_single_experiment(dataset: StandardDataset, model_name: str, hyper_params: dict) -> ExperimentResult:
    """
    执行单轮完整实验，全程受内核约束
    1. 前置宿命边界校验 2. 模型初始化 3. 训练+早停 4. 验证 5. 结果标记 6. 日志留存
    """
    # 第一步：前置边界校验
    budget_used = get_current_budget_used()
    passed, msg = adapter.before_experiment_check({
        "budget_used": budget_used,
        "dataset_source": dataset.dataset_id
    })
    if not passed:
        return ExperimentResult(
            train_status = TrainStatus.BLOCKED_BY_BOUNDARY,
            val_metrics = {}
        )
    
    # 第二步：实例化模型
    model = create_model(model_name, dataset.task_type, hyper_params)
    
    # 第三步：训练+早停
    train_state = {"explore_rate": 0.3, "oscillation_var": 0.0}
    best_val_score = 0.0
    no_improve = 0
    train_metrics_history = []
    
    for epoch in range(hyper_params.get("max_epoch", 200)):
        epoch_metrics = model.train(dataset.train_data, dataset.val_data, hyper_params)
        val_score = model.evaluate(dataset.val_data)
        train_metrics_history.append(epoch_metrics)
        
        # 舒适边界检测，自动调整
        train_state["oscillation_var"] = calc_recent_var(train_metrics_history)
        suggestions = adapter.train_comfort_check(train_state)
        if "damping" in suggestions:
            model.adjust_weight_decay(suggestions["damping"])
        
        # 早停逻辑
        if val_score > best_val_score:
            best_val_score = val_score
            no_improve = 0
            model.save(f"./checkpoints/{exp_id}_best.pt")
        else:
            no_improve += 1
            if no_improve >= hyper_params.get("patience", 15):
                status = TrainStatus.STOPPED_EARLY
                break
    else:
        status = TrainStatus.FINISHED
    
    # 第四步：结果分类标记
    val_truth = adapter.mark_data(best_val_score, "validation_ground_truth")
    pred_result = model.predict(dataset.test_data)
    pred_classified = adapter.mark_data(pred_result, "model_prediction")
    # 自动虚实校准
    calibrated_pred = oce.api.calibrate_illusion(pred_classified, val_truth)
    
    # 第五步：组装结果
    result = ExperimentResult(
        exp_id = generate_id(),
        model_name = model_name,
        dataset_id = dataset.dataset_id,
        hyper_params = hyper_params,
        train_metrics = {"history": train_metrics_history},
        val_metrics = {"score": best_val_score},
        pred_result = calibrated_pred,
        train_status = status,
        cost_budget = 1
    )
    increment_budget_used(1)
    log_audit(f"实验完成: {result.exp_id}, 验证得分: {best_val_score:.4f}")
    return result |
| --- |

| python
def grid_search(dataset: StandardDataset, model_name: str, search_space: dict) -> ExperimentResult:
    """
    网格搜索：遍历所有超参组合，串行执行
    适合小空间基础探索，建立初始基线
    """
    param_list = generate_grid_combinations(search_space)
    best_result = None
    best_score = 0.0
    
    for params in param_list:
        # 宿命边界校验，预算耗尽则终止
        if get_current_budget_used() >= get_total_budget():
            log_audit("预算耗尽，搜索终止")
            break
        result = run_single_experiment(dataset, model_name, params)
        if result.train_status == TrainStatus.BLOCKED_BY_BOUNDARY:
            continue
        if result.val_metrics["score"] > best_score:
            best_score = result.val_metrics["score"]
            best_result = result
    
    log_audit(f"网格搜索完成，最优得分: {best_score:.4f}")
    return best_result |
| --- |

| python
def random_search(dataset: StandardDataset, model_name: str, search_space: dict, n_trials: int) -> ExperimentResult:
    """随机采样超参组合，适合大空间快速探索"""
    best_result = None
    best_score = 0.0
    
    for _ in range(n_trials):
        if get_current_budget_used() >= get_total_budget():
            break
        params = sample_random_params(search_space)
        result = run_single_experiment(dataset, model_name, params)
        if result.train_status == TrainStatus.BLOCKED_BY_BOUNDARY:
            continue
        if result.val_metrics["score"] > best_score:
            best_score = result.val_metrics["score"]
            best_result = result
    
    return best_result |
| --- |

| python
# fo_efs/api.py 对外暴露
from .dataset_loader import load_dataset, StandardDataset
from .model_zoo import create_model, list_models
from .training_pipeline import run_single_experiment, ExperimentResult
from .searcher import grid_search, random_search
from .types import TaskType, TrainStatus |
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

