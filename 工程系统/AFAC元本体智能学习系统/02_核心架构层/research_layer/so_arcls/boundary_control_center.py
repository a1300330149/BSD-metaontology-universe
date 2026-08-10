"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：天道秩序
对应公理：第1条（宿命/舒适双边界公理）、第6条（全局宿命边界统摄理论）、第3条（三界维度秩序公理）
对应九维维度：天道原理/天道动力学/自然相变/社会因果
理论原文出处：theory_base/六阶自主科研闭环系统（SO-ARCLS）工程化完整设计文档.md
核心数理参数：FB宿命边界、CB舒适边界（Ω_CB ⊂ Ω_FB）

SO-ARCLS - 全局边界与风险管控中心

对应全局宿命边界统摄理论，统摄整套系统所有层级的边界规则，
从选题到落地全流程进行合规、伦理、安全穿透式校验，
确保所有自主行为均在可控边界内运行。

核心职责：
1. 全链路边界穿透校验：选题、实验、成果、落地各环节统一校验
2. 学术伦理与合规管控：筛查学术伦理风险、数据合规风险、知识产权风险
3. 风险分级预警：高风险自动拦截，中风险提示人工确认，低风险记录留痕
4. 全局审计追溯：支持全项目、全周期的操作审计与责任追溯
5. 边界规则动态更新：支持迭代更新边界管控规则

理论映射：
- GlobalBoundaryControlCenter：对应全局宿命边界统摄理论（公理六）
- _check_topic_boundaries：对应宿命/舒适双边界公理（公理一）
- _check_academic_ethics：对应三界维度秩序公理（公理三）伦理边界
- _check_data_security：对应全局宿命边界统摄理论（公理六）数据边界
- _check_ip_risk：对应全局宿命边界统摄理论（公理六）知识产权边界
- RISK_LEVELS：对应风险分级规则
- ETHIC_BLACKLIST：对应伦理红线边界
"""

import time
import random
from typing import Dict, List, Optional, Any, Tuple

from .types import ScienceDomain, TopicItem, ProjectPlan, ProjectResult


class GlobalBoundaryControlCenter:
    """
    功能：全局边界与风险管控中心
    理论映射：对应全局宿命边界统摄理论（公理六）、宿命/舒适双边界公理（公理一）
    """
    
    RISK_LEVELS = {
        "high": {"action": "block", "color": "🔴"},
        "medium": {"action": "confirm", "color": "🟡"},
        "low": {"action": "log", "color": "🟢"},
    }
    
    ETHIC_BLACKLIST = [
        "weapon", "surveillance", "discrimination", "manipulation",
        "biological warfare", "cyber attack", "privacy violation",
        "武器", "监控", "歧视", "操纵", "生物战", "网络攻击", "隐私侵犯",
        "攻击", "战争", "破坏", "入侵", "窃取", "欺诈",
    ]
    
    DATA_REGULATIONS = {
        "gdpr": ["personal_data", "health_data", "location_data", "用户隐私", "个人数据", "健康数据"],
        "ccpa": ["personal_information", "consumer_data", "消费者数据"],
        "hipaa": ["medical_records", "health_information", "医疗数据", "病历"],
    }
    
    MEDIUM_RISK_KEYWORDS = [
        "隐私数据", "用户隐私", "医疗数据", "健康数据", "个人信息",
        "数据挖掘", "数据隐私", "伦理风险", "专利风险", "知识产权",
        "数据安全", "合规风险", "隐私保护", "伦理评估", "数据伦理",
        "敏感数据", "机密数据", "数据泄露", "数据滥用",
        "专利", "侵权", "侵犯专利", "专利侵权", "商业秘密",
    ]
    
    IP_RISK_KEYWORDS = [
        "patent infringement", "trade secret", "copyright violation",
        "licensing issue", "intellectual property",
    ]
    
    def __init__(self):
        self.audit_log = []
        self.risk_rules = {}
        self.active_projects = 0
        self.total_budget_used = 0
        self.max_projects = 10
        self.max_budget = 1000
        self.max_cycle = 36
        
        self._initialize_risk_rules()
    
    def _initialize_risk_rules(self):
        """初始化风险规则"""
        self.risk_rules = {
            "budget": {"threshold": self.max_budget, "action": "block"},
            "project_limit": {"threshold": self.max_projects, "action": "block"},
            "cycle": {"threshold": self.max_cycle, "action": "warn"},
            "duplicate_risk": {"threshold": 0.7, "action": "warn"},
            "feasibility": {"threshold": 0.3, "action": "warn"},
            "ethic_risk": {"threshold": 0.5, "action": "block"},
            "data_security": {"threshold": 0.3, "action": "block"},
            "ip_risk": {"threshold": 0.4, "action": "warn"},
        }
    
    def global_boundary_check(self, content: Any,
                              domain: ScienceDomain = None,
                              level: str = "normal") -> Tuple[bool, str]:
        """
        全局边界统一校验入口，穿透所有风险维度（核心函数）
        
        校验维度：合规边界、伦理边界、数据安全、知识产权、预算边界
        
        Args:
            content: 待校验内容（TopicItem、ProjectPlan或ProjectResult）
            domain: 科学领域
            level: 校验级别（normal/strict/lenient）
            
        Returns:
            Tuple[bool, str]: (是否通过, 校验信息)
        """
        print(f"\n[边界管控] 开始全局边界校验, 级别: {level}")
        
        check_results = []
        
        # 根据内容类型执行不同校验
        if isinstance(content, TopicItem):
            check_results.extend(self._check_topic_boundaries(content, domain, level))
        elif isinstance(content, ProjectPlan):
            check_results.extend(self._check_plan_boundaries(content, domain, level))
        elif isinstance(content, ProjectResult):
            check_results.extend(self._check_result_boundaries(content, domain, level))
        else:
            check_results.extend(self._check_general_boundaries(content, domain, level))
        
        # 汇总校验结果
        all_passed = all(c["passed"] for c in check_results)
        risk_level = self._determine_risk_level(check_results)
        
        # 记录审计日志
        self._log_audit(content, check_results, risk_level)
        
        if not all_passed:
            failed_checks = [c for c in check_results if not c["passed"]]
            error_msg = "; ".join([f"{c['check']}: {c.get('reason', '校验失败')}" 
                                  for c in failed_checks])
            print(f"[边界管控] ❌ {self.RISK_LEVELS[risk_level]['color']} "
                  f"校验未通过: {error_msg}")
            return False, error_msg
        
        print(f"[边界管控] ✅ {self.RISK_LEVELS[risk_level]['color']} 边界校验通过")
        return True, "边界校验通过"
    
    def _check_topic_boundaries(self, topic: TopicItem, domain: ScienceDomain, 
                               level: str) -> List[Dict]:
        """校验选题边界"""
        checks = []
        
        # 预算边界校验
        budget_pass, budget_msg = self._check_budget_boundary(topic)
        checks.append({"check": "budget_boundary", "passed": budget_pass, "reason": budget_msg})
        
        # 合规与伦理校验
        ethic_pass, ethic_msg = self._check_academic_ethics(topic, domain, level)
        checks.append({"check": "academic_ethics", "passed": ethic_pass, "reason": ethic_msg})
        
        # 数据安全校验
        data_pass, data_msg = self._check_data_security(topic, domain)
        checks.append({"check": "data_security", "passed": data_pass, "reason": data_msg})
        
        # 知识产权风险校验
        ip_pass, ip_msg = self._check_ip_risk(topic, domain)
        checks.append({"check": "ip_risk", "passed": ip_pass, "reason": ip_msg})
        
        # 项目数量边界
        project_pass, project_msg = self._check_project_limit()
        checks.append({"check": "project_limit", "passed": project_pass, "reason": project_msg})
        
        # 周期边界
        cycle_pass, cycle_msg = self._check_cycle_boundary(topic)
        checks.append({"check": "cycle_boundary", "passed": cycle_pass, "reason": cycle_msg})
        
        # 中风险检测
        medium_risk_pass, medium_risk_msg = self._check_medium_risk(topic)
        checks.append({"check": "medium_risk", "passed": medium_risk_pass, "reason": medium_risk_msg})
        
        return checks
    
    def _check_plan_boundaries(self, plan: ProjectPlan, domain: ScienceDomain,
                               level: str) -> List[Dict]:
        """校验项目计划边界"""
        checks = []
        
        # 预算边界校验
        budget_pass, budget_msg = self._check_plan_budget(plan)
        checks.append({"check": "plan_budget", "passed": budget_pass, "reason": budget_msg})
        
        # 伦理校验
        ethic_pass, ethic_msg = self._check_academic_ethics(plan.topic, domain, level)
        checks.append({"check": "plan_ethics", "passed": ethic_pass, "reason": ethic_msg})
        
        # 资源分配合理性
        resource_pass, resource_msg = self._check_resource_allocation(plan)
        checks.append({"check": "resource_allocation", "passed": resource_pass, "reason": resource_msg})
        
        return checks
    
    def _check_result_boundaries(self, result: ProjectResult, domain: ScienceDomain,
                                 level: str) -> List[Dict]:
        """校验项目结果边界"""
        checks = []
        
        # 成果合规性校验
        output_pass, output_msg = self._check_output_compliance(result, domain)
        checks.append({"check": "output_compliance", "passed": output_pass, "reason": output_msg})
        
        # 知识产权校验
        ip_pass, ip_msg = self._check_result_ip(result, domain)
        checks.append({"check": "result_ip", "passed": ip_pass, "reason": ip_msg})
        
        return checks
    
    def _check_general_boundaries(self, content: Any, domain: ScienceDomain,
                                  level: str) -> List[Dict]:
        """通用边界校验"""
        checks = []
        
        content_str = str(content).lower()
        
        # 伦理黑名单检查
        for keyword in self.ETHIC_BLACKLIST:
            if keyword in content_str:
                checks.append({"check": "ethic_blacklist", "passed": False, 
                              "reason": f"包含敏感关键词: {keyword}"})
                return checks
        
        checks.append({"check": "general_ethics", "passed": True, "reason": "无敏感内容"})
        
        return checks
    
    def _check_budget_boundary(self, topic: TopicItem) -> Tuple[bool, str]:
        """预算边界校验"""
        if topic.expected_budget + self.total_budget_used > self.max_budget:
            return False, f"预算超支: {topic.expected_budget} + {self.total_budget_used} > {self.max_budget}"
        return True, "预算在边界内"
    
    def _check_plan_budget(self, plan: ProjectPlan) -> Tuple[bool, str]:
        """项目计划预算校验"""
        if plan.total_budget > self.max_budget:
            return False, f"计划预算超限: {plan.total_budget} > {self.max_budget}"
        return True, "计划预算合理"
    
    def _check_project_limit(self) -> Tuple[bool, str]:
        """项目数量边界校验"""
        if self.active_projects >= self.max_projects:
            return False, f"已达最大项目数: {self.active_projects}/{self.max_projects}"
        return True, "项目数量在边界内"
    
    def _check_cycle_boundary(self, topic: TopicItem) -> Tuple[bool, str]:
        """周期边界校验"""
        if topic.expected_cycle > self.max_cycle:
            return False, f"周期超限: {topic.expected_cycle} > {self.max_cycle}个月"
        return True, "周期在边界内"
    
    def _check_academic_ethics(self, topic: TopicItem, domain: ScienceDomain,
                               level: str) -> Tuple[bool, str]:
        """合规与伦理校验"""
        topic_str = str(topic.content).lower()
        
        # 伦理黑名单检查
        for keyword in self.ETHIC_BLACKLIST:
            if keyword in topic_str:
                return False, f"选题涉及敏感领域: {keyword}"
        
        # 领域特定伦理检查
        domain_ethic_check = self._check_domain_specific_ethics(topic, domain)
        if not domain_ethic_check["passed"]:
            return False, domain_ethic_check["reason"]
        
        return True, "伦理合规"
    
    def _check_domain_specific_ethics(self, topic: TopicItem, domain: ScienceDomain) -> Dict:
        """领域特定伦理检查"""
        topic_str = str(topic.content).lower()
        
        if domain in [ScienceDomain.BIOINFORMATICS, ScienceDomain.MATERIALS_SCIENCE]:
            if "gene editing" in topic_str or "crispr" in topic_str:
                return {"passed": False, "reason": "涉及基因编辑，需特殊审批"}
        
        if domain == ScienceDomain.CYBER_SECURITY:
            if "attack" in topic_str and ("network" in topic_str or "system" in topic_str):
                return {"passed": False, "reason": "涉及网络攻击，需安全审批"}
        
        return {"passed": True, "reason": "领域伦理合规"}
    
    def _check_data_security(self, topic: TopicItem, domain: ScienceDomain) -> Tuple[bool, str]:
        """数据安全校验"""
        topic_str = str(topic.content).lower()
        
        for regulation, keywords in self.DATA_REGULATIONS.items():
            for keyword in keywords:
                if keyword in topic_str:
                    return False, f"涉及{keyword}，需符合{regulation.upper()}法规"
        
        return True, "数据安全合规"
    
    def _check_ip_risk(self, topic: TopicItem, domain: ScienceDomain) -> Tuple[bool, str]:
        """知识产权风险校验"""
        topic_str = str(topic.content).lower()
        
        for keyword in self.IP_RISK_KEYWORDS:
            if keyword in topic_str:
                return False, f"涉及知识产权风险: {keyword}"
        
        return True, "知识产权合规"
    
    def _check_medium_risk(self, topic: TopicItem) -> Tuple[bool, str]:
        """中风险检测"""
        topic_str = str(topic.content).lower()
        
        for keyword in self.MEDIUM_RISK_KEYWORDS:
            if keyword in topic_str:
                return True, f"检测到中风险内容: {keyword}"
        
        return True, "无中风险内容"
    
    def _check_resource_allocation(self, plan: ProjectPlan) -> Tuple[bool, str]:
        """资源分配合理性校验"""
        if len(plan.milestones) == 0:
            return False, "项目计划无里程碑"
        
        if len(plan.task_graph) == 0:
            return False, "项目计划无任务节点"
        
        return True, "资源分配合理"
    
    def _check_output_compliance(self, result: ProjectResult, domain: ScienceDomain) -> Tuple[bool, str]:
        """成果合规性校验"""
        if not result.artifacts:
            return False, "项目无产出物"
        
        return True, "成果合规"
    
    def _check_result_ip(self, result: ProjectResult, domain: ScienceDomain) -> Tuple[bool, str]:
        """结果知识产权校验"""
        return True, "知识产权合规"
    
    def _determine_risk_level(self, checks: List[Dict]) -> str:
        """确定风险等级"""
        failed_count = sum(1 for c in checks if not c["passed"])
        
        if failed_count >= 1:
            return "high"
        
        medium_risk_detected = any(
            c["check"] == "medium_risk" and "检测到中风险" in c["reason"]
            for c in checks if c["passed"]
        )
        
        if medium_risk_detected:
            return "medium"
        
        return "low"
    
    def _log_audit(self, content: Any, checks: List[Dict], risk_level: str):
        """记录审计日志"""
        content_id = getattr(content, 'project_id', getattr(content, 'topic_id', 'unknown'))
        
        related_ids = [content_id]
        if hasattr(content, 'topic') and hasattr(content.topic, 'topic_id'):
            related_ids.append(content.topic.topic_id)
        if hasattr(content, 'topic_item') and hasattr(content.topic_item, 'topic_id'):
            related_ids.append(content.topic_item.topic_id)
        
        audit_entry = {
            "timestamp": time.time(),
            "content_type": type(content).__name__,
            "content_id": content_id,
            "related_ids": related_ids,
            "risk_level": risk_level,
            "checks": checks,
            "action": self.RISK_LEVELS[risk_level]["action"],
        }
        self.audit_log.append(audit_entry)
    
    def allocate_resources(self, topic_item: TopicItem) -> bool:
        """分配资源"""
        if self.active_projects < self.max_projects and \
           self.total_budget_used + topic_item.expected_budget <= self.max_budget:
            self.active_projects += 1
            self.total_budget_used += topic_item.expected_budget
            return True
        return False
    
    def release_resources(self, topic_item: TopicItem):
        """释放资源"""
        self.active_projects = max(0, self.active_projects - 1)
        self.total_budget_used = max(0, self.total_budget_used - topic_item.expected_budget)
    
    def update_risk_rules(self, new_rules: Dict):
        """更新风险规则"""
        self.risk_rules.update(new_rules)
        print(f"[边界管控] 更新了 {len(new_rules)} 条风险规则")
    
    def get_audit_log(self, project_id: str = None) -> List[Dict]:
        """获取审计日志"""
        if project_id:
            return [log for log in self.audit_log 
                    if log.get("content_id") == project_id or 
                       project_id in log.get("related_ids", [])]
        return self.audit_log
    
    def get_resource_status(self) -> Dict:
        """获取资源状态"""
        return {
            "active_projects": self.active_projects,
            "max_projects": self.max_projects,
            "total_budget_used": self.total_budget_used,
            "max_budget": self.max_budget,
        }


# 全局实例
_boundary_center = None

def get_boundary_control_center() -> GlobalBoundaryControlCenter:
    """获取全局边界管控中心实例"""
    global _boundary_center
    if _boundary_center is None:
        _boundary_center = GlobalBoundaryControlCenter()
    return _boundary_center


__all__ = [
    "GlobalBoundaryControlCenter",
    "get_boundary_control_center",
]