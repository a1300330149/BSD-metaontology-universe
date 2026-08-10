"""
BSD虚拟宇宙时间化模块
[归属基底：L0总本源层·六系核心公理·双时针激活机制·0×0=n定理]
[对应公理：双时针激活公理·生命周期公理·逆时针归零公理·永续追问公理]
[V1.0·2026-08-01·四向展开法·时间化维度]

核心：将静态结构赋予双时针生命周期。
双时针：顺时针积累（0→n→∞）+ 逆时针归零（∞→n→0）。
两者耦合形成0×0=n的永续循环。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum
import time


class LifecyclePhase(str, Enum):
    """实体生命周期相位"""
    EMERGENCE = "emergence"            # 涌现期·0→n·从空无中诞生
    GROWTH = "growth"                  # 成长期·n→∞·顺时针积累中
    STABILITY = "stability"            # 稳定期·n→n·稳态存在
    DECAY = "decay"                    # 衰退期·n→0·属性剥离中
    ZEROING = "zeroing"                # 归零期·0→0∅·逆时针归零
    REBIRTH = "rebirth"                # 重生期·0∅→0→n·完成循环


class ClockState(str, Enum):
    """双时针状态"""
    STOPPED = "stopped"                  # 停止
    CLOCKWISE = "clockwise"              # 顺时针·积累
    COUNTERCLOCKWISE = "counterclockwise"  # 逆时针·归零
    COUPLED = "coupled"                  # 双时针耦合·同步运转


@dataclass
class TimelineEvent:
    """时间线事件"""
    event_id: str
    timestamp: float
    phase: LifecyclePhase
    description: str
    entity_id: str = ""
    scene_id: str = ""
    metadata: Dict = field(default_factory=dict)


@dataclass
class LifecycleState:
    """实体生命周期状态"""
    entity_id: str
    phase: LifecyclePhase = LifecyclePhase.EMERGENCE
    # 各阶段持续时间（秒）
    emergence_duration: float = 10.0
    growth_duration: float = 100.0
    stability_duration: float = 500.0
    decay_duration: float = 50.0
    zeroing_duration: float = 10.0
    # 当前阶段累计时间
    current_phase_time: float = 0.0
    # 是否完成循环
    cycle_count: int = 0
    max_cycles: int = 999
    # 阶段转换回调
    on_phase_transition: Optional[Callable] = None
    # 生命周期历史
    transition_history: List[Dict] = field(default_factory=list)

    def current_duration(self) -> float:
        dur_map = {
            LifecyclePhase.EMERGENCE: self.emergence_duration,
            LifecyclePhase.GROWTH: self.growth_duration,
            LifecyclePhase.STABILITY: self.stability_duration,
            LifecyclePhase.DECAY: self.decay_duration,
            LifecyclePhase.ZEROING: self.zeroing_duration,
            LifecyclePhase.REBIRTH: self.emergence_duration,
        }
        return dur_map.get(self.phase, 10.0)

    def advance(self, delta_time: float) -> Optional[LifecyclePhase]:
        """推进生命周期·返回新相位（若发生转换）"""
        self.current_phase_time += delta_time
        duration = self.current_duration()
        if self.current_phase_time >= duration:
            # 发生相位转换
            old_phase = self.phase
            new_phase = self._next_phase()
            self.transition_history.append({
                "from": old_phase.value,
                "to": new_phase.value,
                "time": self.current_phase_time,
            })
            self.phase = new_phase
            self.current_phase_time = 0.0
            if self.on_phase_transition:
                self.on_phase_transition(old_phase, new_phase)
            return new_phase
        return None

    def _next_phase(self) -> LifecyclePhase:
        phase_order = [
            LifecyclePhase.EMERGENCE,
            LifecyclePhase.GROWTH,
            LifecyclePhase.STABILITY,
            LifecyclePhase.DECAY,
            LifecyclePhase.ZEROING,
            LifecyclePhase.REBIRTH,
        ]
        idx = phase_order.index(self.phase)
        if idx == len(phase_order) - 1:
            # 完成一次循环
            self.cycle_count += 1
            if self.cycle_count >= self.max_cycles:
                return LifecyclePhase.STABILITY  # 达到最大循环，保持稳定
            return LifecyclePhase.EMERGENCE  # 重新涌现
        return phase_order[idx + 1]

    def get_state_description(self) -> str:
        return (f"实体={self.entity_id} | "
                f"相位={self.phase.value} | "
                f"阶段时间={self.current_phase_time:.1f}/{self.current_duration():.1f}s | "
                f"循环次数={self.cycle_count}/{self.max_cycles}")


class BSDTimeline:
    """BSD虚拟宇宙时间线·双时针生命周期管理器
    
    [归属基底：双时针激活机制+0×0=n定理+生命周期公理]
    [对应公理：双时针激活公理·逆时针归零公理·永续追问公理]
    """

    def __init__(self):
        # 双时针状态
        self.clock_state: ClockState = ClockState.STOPPED
        self.clockwise_speed: float = 1.0       # 顺时针速率（倍速）
        self.counterclockwise_speed: float = 1.0  # 逆时针速率（倍速）
        
        # 实体生命周期状态注册表
        self._lifecycle_states: Dict[str, LifecycleState] = {}
        
        # 时间线事件历史
        self._event_history: List[TimelineEvent] = []
        
        # 全局时间
        self._global_time: float = 0.0
        
        # 每周期tick间隔
        self._tick_interval: float = 1.0

    def start_clock(self, mode: ClockState = ClockState.COUPLED):
        """启动双时针"""
        self.clock_state = mode

    def stop_clock(self):
        """停止双时针"""
        self.clock_state = ClockState.STOPPED

    def set_speed(self, clockwise: float = 1.0, counterclockwise: float = 1.0):
        """设置双时针速率"""
        self.clockwise_speed = clockwise
        self.counterclockwise_speed = counterclockwise

    def register_entity_lifecycle(
        self,
        entity_id: str,
        on_transition: Optional[Callable] = None,
        **kwargs,
    ) -> LifecycleState:
        """注册实体的生命周期状态"""
        state = LifecycleState(
            entity_id=entity_id,
            on_phase_transition=on_transition,
            **kwargs,
        )
        self._lifecycle_states[entity_id] = state
        self._log_event(f"Entity {entity_id} lifecycle registered", 
                       LifecyclePhase.EMERGENCE, entity_id)
        return state

    def unregister_entity(self, entity_id: str):
        """注销实体生命周期"""
        if entity_id in self._lifecycle_states:
            del self._lifecycle_states[entity_id]

    def tick(self, delta_time: float = 1.0):
        """推进一个时间tick"""
        if self.clock_state == ClockState.STOPPED:
            return
        
        self._global_time += delta_time
        
        # 根据时针模式计算实际推进时间
        if self.clock_state == ClockState.CLOCKWISE:
            effective_time = delta_time * self.clockwise_speed
            direction = 1
        elif self.clock_state == ClockState.COUNTERCLOCKWISE:
            effective_time = delta_time * self.counterclockwise_speed
            direction = -1
        elif self.clock_state == ClockState.COUPLED:
            # 双时针耦合：顺时针与逆时针同时运行
            # 实际效果：加速涌现+加速归零
            effective_time = delta_time * max(self.clockwise_speed, self.counterclockwise_speed)
            direction = 0  # 双向
        else:
            effective_time = 0
            direction = 0
        
        # 推进所有实体的生命周期
        for entity_id, state in self._lifecycle_states.items():
            new_phase = state.advance(effective_time)
            if new_phase:
                self._log_event(
                    f"Phase transition: {state.phase.value} → {new_phase.value}",
                    new_phase, entity_id,
                )

    def _log_event(self, description: str, phase: LifecyclePhase, 
                   entity_id: str, scene_id: str = ""):
        """记录时间线事件"""
        event = TimelineEvent(
            event_id=f"evt_{len(self._event_history)}",
            timestamp=self._global_time,
            phase=phase,
            description=description,
            entity_id=entity_id,
            scene_id=scene_id,
        )
        self._event_history.append(event)

    def get_lifecycle_state(self, entity_id: str) -> Optional[LifecycleState]:
        return self._lifecycle_states.get(entity_id)

    def get_all_states(self) -> Dict[str, LifecycleState]:
        return dict(self._lifecycle_states)

    def get_event_history(self, limit: int = 50) -> List[TimelineEvent]:
        return self._event_history[-limit:]

    def simulate(self, total_duration: float, tick_interval: float = 1.0) -> Dict:
        """模拟时间线运行"""
        ticks = int(total_duration / tick_interval)
        initial_cycles = {eid: s.cycle_count for eid, s in self._lifecycle_states.items()}
        
        for _ in range(ticks):
            self.tick(tick_interval)
        
        # 汇总结果
        summary = {
            "total_ticks": ticks,
            "total_time": self._global_time,
            "clock_state": self.clock_state.value,
            "entities_processed": len(self._lifecycle_states),
            "cycle_increases": {},
            "event_count": len(self._event_history),
        }
        for eid, state in self._lifecycle_states.items():
            summary["cycle_increases"][eid] = state.cycle_count - initial_cycles.get(eid, 0)
        
        return summary

    def generate_timeline_report(self) -> str:
        lines = []
        lines.append("=" * 70)
        lines.append("BSD虚拟宇宙时间线·双时针生命周期报告")
        lines.append("=" * 70)
        lines.append(f"\n双时针状态：{self.clock_state.value}")
        lines.append(f"全局时间：{self._global_time:.1f}s")
        lines.append(f"顺时针速率：{self.clockwise_speed}x")
        lines.append(f"逆时针速率：{self.counterclockwise_speed}x")
        
        lines.append(f"\n【实体生命周期状态】{len(self._lifecycle_states)}个实体")
        for eid, state in self._lifecycle_states.items():
            lines.append(f"  {state.get_state_description()}")
        
        lines.append(f"\n【事件历史】最近{len(self._event_history)}条")
        for evt in self._event_history[-10:]:
            lines.append(f"  t={evt.timestamp:.1f} | {evt.phase.value} | {evt.description}")
        
        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


# 快速创建生命周期的辅助函数
def create_quick_lifecycle(entity_id: str) -> LifecycleState:
    """快速创建一个标准生命周期配置"""
    return LifecycleState(
        entity_id=entity_id,
        emergence_duration=5.0,
        growth_duration=30.0,
        stability_duration=60.0,
        decay_duration=10.0,
        zeroing_duration=5.0,
        max_cycles=3,
    )


# 模块公开API
__all__ = [
    "LifecyclePhase", "ClockState",
    "TimelineEvent", "LifecycleState",
    "BSDTimeline",
    "create_quick_lifecycle",
]
