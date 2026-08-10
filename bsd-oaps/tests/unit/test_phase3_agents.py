"""
Phase 3 智能体协议层单元测试
- 5个Agent导入+实例化+功能测试
- 3个协议模块功能测试
"""
import os
import sys
import importlib
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


class TestAgentBase:
    """Agent基类测试"""

    def test_base_importable(self):
        """基类可导入"""
        from bsd_agents.base import BSDAgentBase, AgentMessage
        assert BSDAgentBase is not None
        assert AgentMessage is not None

    def test_agent_message_creation(self):
        """消息可创建"""
        from bsd_agents.base import AgentMessage
        msg = AgentMessage(source="A", target="B", content="test")
        assert msg.source == "A"
        assert msg.target == "B"
        assert msg.content == "test"

    def test_base_send_receive(self):
        """基类发送接收消息"""
        from bsd_agents.base import BSDAgentBase
        agent = BSDAgentBase(name="test", description="测试")
        msg = agent.send("target_agent", "hello", "query")
        assert msg.source == "test"
        agent.receive(msg)
        assert len(agent.message_queue) == 1

    def test_base_get_status(self):
        """基类状态获取"""
        from bsd_agents.base import BSDAgentBase
        agent = BSDAgentBase(name="test", description="测试Agent")
        status = agent.get_status()
        assert status["name"] == "test"
        assert "queue_size" in status


class TestMetaOntologyAgent:
    """元本体推演Agent测试"""

    def test_importable(self):
        """可导入"""
        from bsd_agents.meta_ontology_agent import MetaOntologyAgent
        assert MetaOntologyAgent is not None

    def test_instantiation(self):
        """可实例化"""
        from bsd_agents.meta_ontology_agent import MetaOntologyAgent
        agent = MetaOntologyAgent()
        assert agent.name is not None

    def test_list_all_axioms(self):
        """列出全部39条公理"""
        from bsd_agents.meta_ontology_agent import MetaOntologyAgent
        agent = MetaOntologyAgent()
        result = agent.list_all_axioms()
        if isinstance(result, dict):
            total = result.get("total", 0)
        elif isinstance(result, (list, tuple)):
            total = len(result)
        else:
            total = result
        assert total >= 39, f"公理总数不足: {total}"

    def test_verify_hash(self):
        """哈希校验"""
        from bsd_agents.meta_ontology_agent import MetaOntologyAgent
        agent = MetaOntologyAgent()
        result = agent.verify_hash()
        assert result is not None

    def test_bsd_header(self):
        """有BSD标注头"""
        filepath = os.path.join(PROJECT_ROOT, "bsd_agents", "meta_ontology_agent.py")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert "归属基底" in content
        assert "对应公理" in content


class TestTheoryEvolutionAgent:
    """理论演化Agent测试"""

    def test_importable(self):
        from bsd_agents.theory_evolution_agent import TheoryEvolutionAgent
        assert TheoryEvolutionAgent is not None

    def test_instantiation(self):
        from bsd_agents.theory_evolution_agent import TheoryEvolutionAgent
        agent = TheoryEvolutionAgent()
        assert agent.name is not None

    def test_list_mother_disciplines(self):
        """列出母科"""
        from bsd_agents.theory_evolution_agent import TheoryEvolutionAgent
        agent = TheoryEvolutionAgent()
        result = agent.list_mother_disciplines()
        assert result is not None

    def test_bsd_header(self):
        filepath = os.path.join(PROJECT_ROOT, "bsd_agents", "theory_evolution_agent.py")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert "归属基底" in content


class TestApplicationAgent:
    """应用落地Agent测试（含T90 V1.8合规测试）"""

    def test_importable(self):
        from bsd_agents.application_agent import ApplicationAgent
        assert ApplicationAgent is not None

    def test_instantiation(self):
        from bsd_agents.application_agent import ApplicationAgent
        agent = ApplicationAgent()
        assert agent.name is not None

    def test_run_simulation(self):
        """可调用仿真"""
        from bsd_agents.application_agent import ApplicationAgent
        agent = ApplicationAgent()
        result = agent.run_simulation("life_steady", {"qi": 0.7, "blood": 0.8})
        assert result is not None

    def test_bsd_header(self):
        filepath = os.path.join(PROJECT_ROOT, "bsd_agents", "application_agent.py")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert "归属基底" in content

    # ==================================================================
    # T90 V1.8 合规测试
    # ==================================================================

    def test_t90_v18_status_code(self):
        """T90 V1.8 状态码标注"""
        from bsd_agents.application_agent import ApplicationAgent
        agent = ApplicationAgent()
        assert agent.THEORY_VERSION == "ACTIVE-V1.8"

    def test_t90_v18_params_referenced(self):
        """引用7个T90 V1.8锁档参数"""
        from bsd_agents.application_agent import ApplicationAgent
        agent = ApplicationAgent()
        params = agent.T90_V18_PARAMS
        assert params["K_PLUS"] == 0.9
        assert params["K_MINUS"] == 0.1
        assert params["S_ZERO"] == 0.81
        assert params["LAMBDA"] == 0.62
        assert params["LAMBDA_INV"] == 1.38
        assert params["PI_LOCKED"] == 3.1415926535
        assert params["PI_2"] == 2.8274333882

    def test_t90_v18_operators_initialized(self):
        """四大算子模块已初始化"""
        from bsd_agents.application_agent import ApplicationAgent
        agent = ApplicationAgent()
        assert agent.bidirectional_operator is not None
        assert agent.six_level_emergence is not None
        assert agent.three_nine_isomorphism is not None
        assert agent.particle_family_matrix is not None

    def test_dual_clockwise_iteration(self):
        """C1双时针迭代动力学可执行"""
        from bsd_agents.application_agent import ApplicationAgent
        agent = ApplicationAgent()
        result = agent.run_dual_clockwise_iteration()
        assert result is not None
        assert result["scene"] == "dual_clockwise_iteration"
        assert result["theory_version"] == "ACTIVE-V1.8"
        # 对偶性定理11.19校验通过
        iter_res = result["iteration_result"]
        assert iter_res["duality_theorem_11_19"]["passed"] is True
        # 信息痕迹守恒律推论11.9校验通过
        assert iter_res["info_trace_corollary_11_9"]["passed"] is True
        # 升维验证
        assert iter_res["ascension_verified"] is True

    def test_get_t90_v18_status(self):
        """T90 V1.8合规状态可获取"""
        from bsd_agents.application_agent import ApplicationAgent
        agent = ApplicationAgent()
        status = agent.get_t90_v18_status()
        assert status["theory_version"] == "ACTIVE-V1.8"
        assert status["params_verified"] is True
        assert status["all_operators_valid"] is True
        # 四大算子全部自检通过
        ops = status["operators"]
        assert ops["C1_bidirectional_iteration"]["validated"] is True
        assert ops["C2_six_level_emergence"]["validated"] is True
        assert ops["C3_three_nine_isomorphism"]["validated"] is True
        assert ops["C5_particle_family_matrix"]["validated"] is True

    def test_copyright_info(self):
        """版权确权信息完整"""
        from bsd_agents.application_agent import ApplicationAgent
        agent = ApplicationAgent()
        copyright_info = agent.COPYRIGHT
        assert copyright_info["author"] == "杨腾飞"
        assert copyright_info["author_id"] == "433127199812193215"
        assert copyright_info["hash_sha256"] is not None
        assert len(copyright_info["hash_sha256"]) > 0
        assert copyright_info["lock_date"] == "2026-06-20"
        assert "杨腾飞" in copyright_info["equity_split"]

    def test_medicine_result_includes_t90_params(self):
        """医学场景结果包含T90 V1.8参数"""
        from bsd_agents.application_agent import ApplicationAgent
        agent = ApplicationAgent()
        result = agent.apply_to_medicine({"qi": 0.8, "blood": 0.8, "body": 0.8, "mind": 0.8, "dao": 0.8})
        assert "t90_v18_params" in result
        assert result["theory_version"] == "ACTIVE-V1.8"
        assert "s_zero_threshold" in result
        assert result["s_zero_threshold"] == 0.81

    def test_file_contains_t90_v18_markers(self):
        """文件包含T90 V1.8标记"""
        filepath = os.path.join(PROJECT_ROOT, "bsd_agents", "application_agent.py")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert "ACTIVE-V1.8" in content
        assert "K_PLUS" in content
        assert "K_MINUS" in content
        assert "S_ZERO" in content
        assert "BidirectionalIterationOperator" in content
        assert "SixLevelBaseEmergence" in content
        assert "ThreeNineIsomorphism" in content
        assert "ParticleFamilyMatrix" in content
        assert "run_dual_clockwise_iteration" in content
        assert "确权" in content


class TestCrossValidationAgent:
    """交叉验证Agent测试"""

    def test_importable(self):
        from bsd_agents.cross_validation_agent import CrossValidationAgent
        assert CrossValidationAgent is not None

    def test_instantiation(self):
        from bsd_agents.cross_validation_agent import CrossValidationAgent
        agent = CrossValidationAgent()
        assert agent.name is not None

    def test_run_full_validation(self):
        """可执行全套验证"""
        from bsd_agents.cross_validation_agent import CrossValidationAgent
        agent = CrossValidationAgent()
        result = agent.run_full_validation()
        assert result is not None

    def test_bsd_header(self):
        filepath = os.path.join(PROJECT_ROOT, "bsd_agents", "cross_validation_agent.py")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert "归属基底" in content


class TestMillenniumAgent:
    """千禧年难题验证Agent测试"""

    def test_importable(self):
        from bsd_agents.millennium_agent import MillenniumAgent
        assert MillenniumAgent is not None

    def test_instantiation(self):
        from bsd_agents.millennium_agent import MillenniumAgent
        agent = MillenniumAgent()
        assert agent.name is not None

    def test_verify_single_problem(self):
        """可验证单个难题"""
        from bsd_agents.millennium_agent import MillenniumAgent
        agent = MillenniumAgent()
        result = agent.verify("p_vs_np")
        assert result is not None
        assert isinstance(result, dict)

    def test_verify_all(self):
        """可验证全部难题"""
        from bsd_agents.millennium_agent import MillenniumAgent
        agent = MillenniumAgent()
        result = agent.verify_all()
        assert result is not None
        assert isinstance(result, dict)
        # verify_all返回汇总dict，包含results子字典或total字段
        if "results" in result:
            assert len(result["results"]) >= 8
        elif "total" in result:
            assert result["total"] >= 8
        else:
            assert len(result) >= 8

    def test_bsd_header(self):
        filepath = os.path.join(PROJECT_ROOT, "bsd_agents", "millennium_agent.py")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert "归属基底" in content
        assert "T87" in content or "千禧" in content


class TestProtocols:
    """通信协议模块测试"""

    def test_agent_message_importable(self):
        """消息格式模块可导入"""
        from bsd_agents.protocols.agent_message import create_message, validate_message
        assert create_message is not None
        assert validate_message is not None

    def test_create_message(self):
        """可创建消息"""
        from bsd_agents.protocols.agent_message import create_message
        msg = create_message("A", "B", "QUERY", {"action": "test"})
        assert msg is not None

    def test_task_dispatcher(self):
        """任务调度器可使用"""
        from bsd_agents.protocols.task_dispatch import TaskDispatcher
        from bsd_agents.meta_ontology_agent import MetaOntologyAgent
        dispatcher = TaskDispatcher()
        agent = MetaOntologyAgent()
        dispatcher.register_agent("meta_ontology", agent)
        agents = dispatcher.list_agents()
        assert "meta_ontology" in agents

    def test_result_aggregator(self):
        """结果聚合器可使用"""
        from bsd_agents.protocols.result_aggregation import ResultAggregator
        agg = ResultAggregator()
        agg.collect("task1", "agent1", {"status": "ok"})
        agg.collect("task1", "agent2", {"status": "ok"})
        summary = agg.get_summary("task1")
        assert summary is not None

    def test_protocol_bsd_headers(self):
        """协议模块有BSD标注"""
        files = [
            "bsd_agents/protocols/agent_message.py",
            "bsd_agents/protocols/task_dispatch.py",
            "bsd_agents/protocols/result_aggregation.py",
        ]
        for f in files:
            full = os.path.join(PROJECT_ROOT, f)
            with open(full, "r", encoding="utf-8") as fp:
                content = fp.read()
            assert "归属基底" in content, f"{f} 缺少BSD标注头"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
