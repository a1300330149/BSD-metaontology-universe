"""
归属基底：第0重元道本源基底 + BSD六系立系引擎论
对应公理：全域公理 + 引擎同构公理 + 六阶闭环公理
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/
固定数理常量：γ=0.92, κ=0.35

BSD Agent 基类 — 集成六阶引擎
"""
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
from enum import Enum
import time
import uuid


# ============================================================
# 六阶状态定义
# ============================================================

class SixStageStatus(Enum):
    """六阶状态"""
    IDLE = "空闲"
    CONNECTING = "连接中"
    ACTIVATING = "激活中"
    FUSING = "融合中"
    UPGRADING = "升维中"
    EQUILIBRIUM = "等算中"
    METAMORPHOSIS = "计变中"
    COMPLETED = "已完成"


class SixSystem(Enum):
    """六系定义"""
    QIANGHUA = "强化系🔵"    # 连接
    ZIRAN = "自然系🟠"       # 激活
    JUXIAN = "具现系🔴"     # 融合
    BIANSHEN = "变身系⚫"    # 升维
    SHEHUI = "社会系🟢"      # 等算
    TIANDAO = "天道系🟣"    # 计变


# ============================================================
# 六阶配置
# ============================================================

SIX_STAGE_CONFIG = {
    'stage_1_connect': {
        'name': '连接',
        'system': SixSystem.QIANGHUA,
        'description': '聚合子引擎，建立连接',
    },
    'stage_2_activate': {
        'name': '激活',
        'system': SixSystem.ZIRAN,
        'description': '激活引擎能力，启动系统',
    },
    'stage_3_fuse': {
        'name': '融合',
        'system': SixSystem.JUXIAN,
        'description': '融合子引擎，形成整体',
    },
    'stage_4_upgrade': {
        'name': '升维',
        'system': SixSystem.BIANSHEN,
        'description': '升维系统能级，突破瓶颈',
    },
    'stage_5_equilibrium': {
        'name': '等算',
        'system': SixSystem.SHEHUI,
        'description': '维持系统秩序，实现计算引力',
    },
    'stage_6_metamorphosis': {
        'name': '计变',
        'system': SixSystem.TIANDAO,
        'description': '产生新变化，触发永动',
    },
}


# ============================================================
# 记忆锚点
# ============================================================

@dataclass
class MemoryAnchor:
    """记忆锚点"""
    anchor_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    keywords: List[str] = field(default_factory=list)
    anchor_type: str = "decision"  # decision, turning_point, keyword, emotion
    weight: float = 1.0
    associated_anchors: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


# ============================================================
# Agent消息
# ============================================================

@dataclass
class AgentMessage:
    """Agent间通信消息"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = ""
    target: str = ""
    message_type: str = ""  # query, response, task, result
    content: Any = None
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# BSD Agent 基类（集成六阶引擎）
# ============================================================

class BSDAgentBase:
    """BSD Agent 基类 — 集成六阶引擎
    
    核心特性：
    1. 六阶闭环支持：连接→激活→融合→升维→等算→计变
    2. 记忆系统：脉络蒸馏→关键词锚定→高效回忆
    3. 实践-认识循环：认识→实践→再认识
    4. 引擎同构：母引擎-子引擎关系
    """
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.message_queue: List[AgentMessage] = []
        
        # ====== 六阶引擎集成 ======
        # 六阶状态
        self._stage_status: SixStageStatus = SixStageStatus.IDLE
        self._current_stage: int = 0
        self._completed_stages: List[int] = []
        self._stage_outputs: Dict[str, Any] = {}
        
        # 记忆系统
        self._memory_anchors: Dict[str, MemoryAnchor] = {}
        self._keyword_index: Dict[str, List[str]] = {}
        
        # 子引擎注册表
        self._sub_engines: Dict[str, Dict] = {}
        
        # 循环计数
        self._cycle_count: int = 0
        self._max_cycles: int = 100
        
        # 统计信息
        self._stats: Dict[str, Any] = {
            'messages_processed': 0,
            'stages_completed': 0,
            'cycles_completed': 0,
            'anchors_created': 0,
            'start_time': time.time(),
        }
    
    # ==================== 消息处理 ====================
    
    def receive(self, message: AgentMessage) -> None:
        """接收消息"""
        self.message_queue.append(message)
    
    def send(self, target: str, content: Any, message_type: str = "query") -> AgentMessage:
        """发送消息"""
        msg = AgentMessage(source=self.name, target=target, 
                          message_type=message_type, content=content)
        return msg
    
    def process(self) -> Any:
        """处理消息队列中的消息（子类实现）"""
        raise NotImplementedError
    
    # ==================== 六阶引擎核心 ====================
    
    def run_six_stages(self, callback: Optional[callable] = None) -> Dict[str, Any]:
        """运行六阶闭环
        
        Args:
            callback: 可选的阶段回调函数
            
        Returns:
            六阶执行结果
        """
        print(f"\n{'='*50}")
        print(f"【{self.name} · 六阶闭环启动】")
        print(f"{'='*50}")
        
        # 重置状态
        self._reset_stage_state()
        self._cycle_count += 1
        
        # 执行六阶
        for stage_id, stage_config in SIX_STAGE_CONFIG.items():
            stage_num = int(stage_id.split('_')[1])
            stage_result = self._execute_stage(stage_num, stage_config, callback)
            
            if not stage_result['success']:
                print(f"    ❌ {stage_config['name']} 失败，中断六阶闭环")
                return self._get_failed_result(stage_config['name'])
        
        # 完成
        self._stage_status = SixStageStatus.COMPLETED
        self._stats['cycles_completed'] += 1
        
        result = self._get_cycle_result()
        print(f"\n  ✅ 六阶闭环完成 (第{self._cycle_count}轮)")
        
        return result
    
    def _execute_stage(self, stage_num: int, stage_config: Dict, 
                      callback: Optional[callable] = None) -> Dict[str, Any]:
        """执行单个阶段"""
        stage_name = stage_config['name']
        stage_system = stage_config['system'].value
        
        print(f"\n  【{stage_name}】({stage_system})")
        
        # 更新状态
        self._current_stage = stage_num
        self._stage_status = SixStageStatus(list(SixStageStatus)[stage_num])
        
        # 调用回调
        stage_data = {
            'stage_num': stage_num,
            'stage_name': stage_name,
            'stage_system': stage_system,
            'agent': self.name,
        }
        
        if callback:
            try:
                callback(stage_data)
            except Exception as e:
                print(f"    ⚠️ 回调执行异常: {e}")
        
        # 阶段逻辑（子类可重写）
        stage_output = self._stage_logic(stage_num, stage_config)
        
        # 保存输出
        self._stage_outputs[stage_name] = stage_output
        self._completed_stages.append(stage_num)
        self._stats['stages_completed'] += 1
        
        print(f"    ✅ 完成")
        
        return {
            'success': True,
            'stage': stage_name,
            'output': stage_output,
        }
    
    def _stage_logic(self, stage_num: int, stage_config: Dict) -> Dict[str, Any]:
        """阶段逻辑（子类可重写）
        
        六阶映射：
        1. 连接(强化系) → 聚合子引擎，建立连接
        2. 激活(自然系) → 激活引擎能力
        3. 融合(具现系) → 融合子引擎
        4. 升维(变身系) → 升维系统能级
        5. 等算(社会系) → 维持秩序，计算引力
        6. 计变(天道系) → 产生新变化
        """
        stage_name = stage_config['name']
        
        # 默认实现（子类可重写）
        default_outputs = {
            1: {'connected_engines': len(self._sub_engines)},
            2: {'capabilities_activated': True},
            3: {'fusion_completed': True},
            4: {'level_upgraded': True},
            5: {'gravity_computed': True},
            6: {'change_generated': True},
        }
        
        return default_outputs.get(stage_num, {})
    
    def _reset_stage_state(self) -> None:
        """重置六阶状态"""
        self._stage_status = SixStageStatus.IDLE
        self._current_stage = 0
        self._completed_stages = []
        self._stage_outputs = {}
    
    def _get_cycle_result(self) -> Dict[str, Any]:
        """获取循环结果"""
        return {
            'agent_name': self.name,
            'cycle': self._cycle_count,
            'stages_completed': self._completed_stages,
            'all_stages_completed': len(self._completed_stages) == 6,
            'outputs': self._stage_outputs,
            'memory_anchors': len(self._memory_anchors),
            'sub_engines': len(self._sub_engines),
        }
    
    def _get_failed_result(self, failed_stage: str) -> Dict[str, Any]:
        """获取失败结果"""
        return {
            'agent_name': self.name,
            'cycle': self._cycle_count,
            'failed_stage': failed_stage,
            'stages_completed': self._completed_stages,
            'success': False,
        }
    
    # ==================== 子引擎管理 ====================
    
    def register_sub_engine(self, engine_id: str, engine_info: Dict) -> str:
        """注册子引擎
        
        Args:
            engine_id: 引擎标识
            engine_info: 引擎信息
            
        Returns:
            注册ID
        """
        reg_id = str(uuid.uuid4())
        self._sub_engines[reg_id] = {
            'engine_id': engine_id,
            'engine_info': engine_info,
            'registered_at': time.time(),
        }
        print(f"  🔗 子引擎已注册: {engine_id}")
        return reg_id
    
    def get_sub_engines(self) -> Dict[str, Dict]:
        """获取所有子引擎"""
        return self._sub_engines
    
    def get_engine_count(self) -> int:
        """获取子引擎数量"""
        return len(self._sub_engines)
    
    # ==================== 记忆系统 ====================
    
    def create_memory_anchor(self, content: str, keywords: List[str],
                            anchor_type: str = "decision") -> str:
        """创建记忆锚点
        
        Args:
            content: 锚点内容
            keywords: 关键词列表
            anchor_type: 锚点类型
            
        Returns:
            锚点ID
        """
        anchor = MemoryAnchor(
            content=content,
            keywords=keywords,
            anchor_type=anchor_type,
        )
        
        self._memory_anchors[anchor.anchor_id] = anchor
        self._stats['anchors_created'] += 1
        
        # 建立关键词索引
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower not in self._keyword_index:
                self._keyword_index[keyword_lower] = []
            self._keyword_index[keyword_lower].append(anchor.anchor_id)
        
        return anchor.anchor_id
    
    def recall_by_keywords(self, query: str, max_results: int = 10) -> List[MemoryAnchor]:
        """通过关键词高效回忆
        
        Args:
            query: 查询字符串
            max_results: 最大返回数
            
        Returns:
            相关锚点列表
        """
        results = []
        query_lower = query.lower()
        
        # 关键词匹配
        for keyword, anchor_ids in self._keyword_index.items():
            if keyword in query_lower:
                for anchor_id in anchor_ids:
                    if anchor_id in self._memory_anchors:
                        results.append(self._memory_anchors[anchor_id])
        
        return results[:max_results]
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        return {
            'total_anchors': len(self._memory_anchors),
            'total_keywords': len(self._keyword_index),
        }
    
    # ==================== 实践-认识循环 ====================
    
    def run_practice_cycle(self, input_data: Any = None) -> Dict[str, Any]:
        """运行实践-认识循环
        
        循环：认识→实践→再认识→再实践→...
        
        Args:
            input_data: 输入数据
            
        Returns:
            循环结果
        """
        print(f"\n  📜 认识阶段: 感知输入...")
        
        # 认识阶段
        knowledge = self._stage_logic(1, SIX_STAGE_CONFIG['stage_1_connect'])
        print(f"    已感知: {knowledge}")
        
        # 实践阶段
        print(f"\n  📜 实践阶段: 执行任务...")
        result = self.run_six_stages()
        
        # 再认识阶段
        print(f"\n  📜 再认识阶段: 分析结果...")
        analysis = {
            'cycle': self._cycle_count,
            'stages_completed': result.get('stages_completed', []),
            'outputs': result.get('outputs', {}),
        }
        
        # 创建记忆锚点
        self.create_memory_anchor(
            content=f"实践-认识循环第{self._cycle_count}轮",
            keywords=['实践', '认识', '循环', str(self._cycle_count)],
            anchor_type='cycle',
        )
        
        return {
            'cycle': self._cycle_count,
            'knowledge': knowledge,
            'practice_result': result,
            'analysis': analysis,
        }
    
    # ==================== 状态查询 ====================
    
    def get_status(self) -> Dict[str, Any]:
        """获取Agent完整状态"""
        return {
            'name': self.name,
            'description': self.description,
            # 六阶状态
            'stage_status': self._stage_status.value,
            'current_stage': self._current_stage,
            'completed_stages': self._completed_stages,
            'cycle_count': self._cycle_count,
            # 引擎状态
            'sub_engines': len(self._sub_engines),
            # 记忆状态
            'memory_anchors': len(self._memory_anchors),
            # 消息状态
            'queue_size': len(self.message_queue),
            # 统计
            'stats': self._stats,
        }
    
    def get_stage_status_text(self) -> str:
        """获取当前阶段文本"""
        status_map = {
            SixStageStatus.IDLE: "💤 空闲",
            SixStageStatus.CONNECTING: "🔗 连接中",
            SixStageStatus.ACTIVATING: "⚡ 激活中",
            SixStageStatus.FUSING: "🔴 融合中",
            SixStageStatus.UPGRADING: "⚫ 升维中",
            SixStageStatus.EQUILIBRIUM: "🟢 等算中",
            SixStageStatus.METAMORPHOSIS: "🟣 计变中",
            SixStageStatus.COMPLETED: "✅ 已完成",
        }
        return status_map.get(self._stage_status, "❓ 未知")


# ============================================================
# 使用示例
# ============================================================

def demo_usage():
    """演示如何使用集成六阶引擎的Agent"""
    
    print("=" * 60)
    print("【BSD Agent · 六阶引擎集成演示】")
    print("=" * 60)
    
    # 1. 创建Agent
    agent = BSDAgentBase(name="TestAgent", description="测试Agent")
    print(f"\n📜 创建Agent: {agent.name}")
    
    # 2. 注册子引擎
    print("\n📜 注册子引擎")
    agent.register_sub_engine("engine_go", {"type": "go", "stages": [1, 2, 3]})
    agent.register_sub_engine("engine_gene", {"type": "gene", "stages": [2, 3, 4]})
    print(f"  子引擎数量: {agent.get_engine_count()}")
    
    # 3. 创建记忆锚点
    print("\n📜 创建记忆锚点")
    anchor_id = agent.create_memory_anchor(
        content="六阶闭环的核心是连接→激活→融合→升维→等算→计变",
        keywords=["六阶", "闭环", "永动", "引擎"],
        anchor_type="decision",
    )
    print(f"  锚点ID: {anchor_id[:8]}...")
    
    # 4. 高效回忆
    print("\n📜 高效回忆测试")
    results = agent.recall_by_keywords("六阶闭环")
    print(f"  找到 {len(results)} 个相关锚点")
    
    # 5. 运行六阶闭环
    print("\n📜 运行六阶闭环")
    
    def stage_callback(stage_data):
        print(f"    📌 阶段回调: {stage_data['stage_name']}")
    
    result = agent.run_six_stages(callback=stage_callback)
    print(f"  六阶完成: {result['all_stages_completed']}")
    
    # 6. 运行实践-认识循环
    print("\n📜 运行实践-认识循环")
    for i in range(3):
        cycle_result = agent.run_practice_cycle()
        print(f"  第{i+1}轮循环完成")
    
    # 7. 获取最终状态
    print("\n📜 Agent最终状态")
    status = agent.get_status()
    print(f"  名称: {status['name']}")
    print(f"  阶段状态: {agent.get_stage_status_text()}")
    print(f"  完成阶段: {status['completed_stages']}")
    print(f"  循环次数: {status['cycle_count']}")
    print(f"  子引擎: {status['sub_engines']}")
    print(f"  记忆锚点: {status['memory_anchors']}")
    
    print("\n" + "=" * 60)
    print("【BSD Agent · 六阶引擎集成演示完成】")
    print("=" * 60)


if __name__ == "__main__":
    demo_usage()
