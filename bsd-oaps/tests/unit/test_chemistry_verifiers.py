"""
归属基底：第0重元道本源基底
对应公理：公理七（系统自进化迭代）
对应九维维度：元理天道
理论原文出处：T87第二十七章 BSD化学全域难题统一实证
固定数理常量：γ=0.92, κ=0.35, α=0.18

化学全域难题单元测试
—— 14个化学难题验证器 + 化学验证Agent
"""
import os
import sys
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


BASIC_PROBLEMS = [
    ("protein_folding", "蛋白质折叠问题", "basic"),
    ("high_tc_superconduct", "高温超导机理", "basic"),
    ("quantum_many_body", "量子化学多体问题", "basic"),
    ("origin_of_life", "生命起源化学", "basic"),
    ("self_assembly", "分子识别与自组装", "basic"),
    ("nonequilibrium_chem", "非平衡态热力学化学", "basic"),
    ("catalysis_mechanism", "均相催化机理", "basic"),
]

ENGINEERING_PROBLEMS = [
    ("artificial_photo", "人工光合作用", "engineering"),
    ("room_temp_super", "室温超导材料", "engineering"),
    ("inverse_catalyst", "催化剂逆设计", "engineering"),
    ("carbon_capture", "碳捕获与高效转化", "engineering"),
    ("high_energy_battery", "高能量密度电池", "engineering"),
    ("green_chemistry", "绿色化学全流程替代", "engineering"),
    ("precision_synthesis", "精准合成/分子手术", "engineering"),
]

ALL_PROBLEMS = BASIC_PROBLEMS + ENGINEERING_PROBLEMS


def get_all_verifiers():
    """获取所有14个化学验证器实例"""
    from bsd_verify.chemistry import get_all_chemistry_verifiers
    return get_all_chemistry_verifiers()


class TestChemistryVerifiersExist:
    """测试14个验证器都能实例化"""

    def test_all_14_verifiers_exist(self):
        """14个验证器全部存在且可实例化"""
        verifiers = get_all_verifiers()
        assert len(verifiers) == 14
        for key, v in verifiers.items():
            assert v is not None
            assert hasattr(v, "verify")
            assert hasattr(v, "get_proof_chain")
            assert hasattr(v, "get_summary")

    def test_verifier_have_required_attributes(self):
        """所有验证器都有必需的属性"""
        verifiers = get_all_verifiers()
        for key, v in verifiers.items():
            assert hasattr(v, "problem_name")
            assert hasattr(v, "bsd_derivation_path")
            assert hasattr(v, "category")
            assert hasattr(v, "nobel_prize_related")
            assert hasattr(v, "industry_value")


class TestChemistryVerifiersRun:
    """测试每个验证器verify()返回正确格式"""

    def test_all_14_run_successfully(self):
        """14个验证器全部可正常运行"""
        verifiers = get_all_verifiers()
        results = {}
        for key, v in verifiers.items():
            result = v.verify()
            results[key] = result
            assert result is not None, f"{key} 返回None"
            assert result.problem_name is not None
            assert isinstance(result.verdict, str) and len(result.verdict) > 0, \
                f"{key} 空verdict"
            assert 0.0 <= result.confidence <= 1.0
            assert result.verification_time >= 0.0
        assert len(results) == 14

    def test_return_type_is_verification_result(self):
        """返回值是 VerificationResult 类型"""
        from bsd_verify.base import VerificationResult
        verifiers = get_all_verifiers()
        for key, v in verifiers.items():
            result = v.verify()
            assert isinstance(result, VerificationResult), f"{key} 返回类型错误"


class TestProofChain:
    """测试证明链非空且至少4步"""

    def test_proof_chain_non_empty(self):
        """所有验证器都有非空证明链"""
        verifiers = get_all_verifiers()
        for key, v in verifiers.items():
            result = v.verify()
            chain = result.proof_chain
            assert isinstance(chain, list), f"{key} proof_chain不是list"
            assert len(chain) >= 4, f"{key} proof_chain少于4步: {len(chain)}"

    def test_proof_chain_steps_have_correct_structure(self):
        """证明链每步都有正确结构"""
        verifiers = get_all_verifiers()
        for key, v in verifiers.items():
            result = v.verify()
            for i, step in enumerate(result.proof_chain):
                assert isinstance(step, dict), f"{key} 第{i}步不是dict"
                assert "step" in step, f"{key} 第{i}步缺少step字段"
                assert "title" in step, f"{key} 第{i}步缺少title字段"
                assert "description" in step, f"{key} 第{i}步缺少description字段"
                assert "equation" in step, f"{key} 第{i}步缺少equation字段"
                assert "evidence" in step, f"{key} 第{i}步缺少evidence字段"


class TestConfidenceRange:
    """测试置信度在合理范围(0.8~1.0)"""

    def test_confidence_in_reasonable_range(self):
        """所有验证器的置信度都在 0.8 ~ 1.0 之间"""
        verifiers = get_all_verifiers()
        for key, v in verifiers.items():
            result = v.verify()
            assert result.confidence >= 0.8, \
                f"{key} 置信度过低: {result.confidence}"
            assert result.confidence <= 1.0, \
                f"{key} 置信度过高: {result.confidence}"

    def test_confidence_not_exactly_same(self):
        """置信度有随机扰动，不完全固定"""
        verifiers = get_all_verifiers()
        confidences = []
        for key, v in verifiers.items():
            result = v.verify()
            confidences.append(result.confidence)
        unique_confs = set(round(c, 8) for c in confidences)
        assert len(unique_confs) > 1, "所有置信度都完全相同，缺少随机扰动"


class TestCategoryCorrect:
    """测试基础类和工程类分类正确"""

    def test_basic_category_correct(self):
        """基础理论类验证器的 category 都是 'basic'"""
        verifiers = get_all_verifiers()
        for key, name, expected_cat in BASIC_PROBLEMS:
            v = verifiers[key]
            assert v.category == expected_cat, \
                f"{key} category错误: {v.category}, 期望: {expected_cat}"
            assert v.nobel_prize_related is True, \
                f"{key} nobel_prize_related应为True"

    def test_engineering_category_correct(self):
        """工程悬赏类验证器的 category 都是 'engineering'"""
        verifiers = get_all_verifiers()
        for key, name, expected_cat in ENGINEERING_PROBLEMS:
            v = verifiers[key]
            assert v.category == expected_cat, \
                f"{key} category错误: {v.category}, 期望: {expected_cat}"
            assert v.nobel_prize_related is False, \
                f"{key} nobel_prize_related应为False"

    def test_7_basic_7_engineering(self):
        """恰好7个基础理论类和7个工程悬赏类"""
        verifiers = get_all_verifiers()
        basic_count = sum(1 for v in verifiers.values() if v.category == "basic")
        eng_count = sum(1 for v in verifiers.values() if v.category == "engineering")
        assert basic_count == 7, f"基础理论类数量错误: {basic_count}"
        assert eng_count == 7, f"工程悬赏类数量错误: {eng_count}"


class TestKeyEquationAndNumerical:
    """测试关键方程和数值证据"""

    def test_key_equation_present(self):
        """所有验证器都有关键方程"""
        verifiers = get_all_verifiers()
        for key, v in verifiers.items():
            result = v.verify()
            assert result.key_equation and len(result.key_equation) > 0, \
                f"{key} 缺少key_equation"

    def test_numerical_evidence_present(self):
        """所有验证器都有数值证据"""
        verifiers = get_all_verifiers()
        for key, v in verifiers.items():
            result = v.verify()
            assert isinstance(result.numerical_evidence, dict), \
                f"{key} numerical_evidence不是dict"
            assert len(result.numerical_evidence) > 0, \
                f"{key} numerical_evidence为空"


class TestChemistryAgent:
    """测试化学验证Agent"""

    def test_agent_can_be_instantiated(self):
        """化学Agent可实例化"""
        from bsd_agents.chemistry_agent import ChemistryVerificationAgent
        agent = ChemistryVerificationAgent()
        assert agent is not None
        assert agent.name == "ChemistryVerificationAgent"

    def test_agent_verify_all(self):
        """Agent verify_all 返回正确格式"""
        from bsd_agents.chemistry_agent import ChemistryVerificationAgent
        agent = ChemistryVerificationAgent()
        result = agent.verify_all()
        assert result["total"] == 14
        assert "passed" in result
        assert "results" in result
        assert len(result["results"]) == 14
        assert "overall_confidence" in result
        assert 0.0 <= result["overall_confidence"] <= 1.0

    def test_agent_verify_category_basic(self):
        """Agent verify_category('basic') 返回7个基础题"""
        from bsd_agents.chemistry_agent import ChemistryVerificationAgent
        agent = ChemistryVerificationAgent()
        result = agent.verify_category("basic")
        assert result["category"] == "basic"
        assert result["total"] == 7
        assert len(result["results"]) == 7

    def test_agent_verify_category_engineering(self):
        """Agent verify_category('engineering') 返回7个工程题"""
        from bsd_agents.chemistry_agent import ChemistryVerificationAgent
        agent = ChemistryVerificationAgent()
        result = agent.verify_category("engineering")
        assert result["category"] == "engineering"
        assert result["total"] == 7
        assert len(result["results"]) == 7

    def test_agent_verify_single_problem(self):
        """Agent 可验证单个难题"""
        from bsd_agents.chemistry_agent import ChemistryVerificationAgent
        agent = ChemistryVerificationAgent()
        result = agent.verify("protein_folding")
        assert result["problem"] == "protein_folding"
        assert "verdict" in result
        assert "confidence" in result
        assert "proof_chain" in result

    def test_agent_verify_unknown_problem(self):
        """Agent 验证未知问题返回错误"""
        from bsd_agents.chemistry_agent import ChemistryVerificationAgent
        agent = ChemistryVerificationAgent()
        result = agent.verify("nonexistent_problem")
        assert result["verdict"] == "unknown"
        assert "error" in result

    def test_agent_get_summary(self):
        """Agent get_summary 返回正确格式"""
        from bsd_agents.chemistry_agent import ChemistryVerificationAgent
        agent = ChemistryVerificationAgent()
        agent.verify_all()
        summary = agent.get_summary()
        assert summary["total"] == 14
        assert "basic" in summary
        assert "engineering" in summary
        assert summary["basic"]["total"] == 7
        assert summary["engineering"]["total"] == 7
        assert "overall_confidence" in summary

    def test_agent_process_message(self):
        """Agent process 可处理消息队列"""
        from bsd_agents.chemistry_agent import ChemistryVerificationAgent
        from bsd_agents.base import AgentMessage
        agent = ChemistryVerificationAgent()
        msg = AgentMessage(
            source="test",
            target="ChemistryVerificationAgent",
            message_type="query",
            content={"action": "verify_all"},
        )
        agent.receive(msg)
        results = agent.process()
        assert len(results) == 1
        assert results[0]["action"] == "verify_all"
        assert "result" in results[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-s"])
