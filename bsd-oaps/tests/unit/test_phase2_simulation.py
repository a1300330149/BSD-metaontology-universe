"""
Phase 2 仿真引擎单元测试
- 8个仿真器可导入+可运行测试
- 4个可视化模块可导入测试
- 仿真结果合理性测试
"""
import os
import sys
import importlib
import numpy as np
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


class TestSimulatorImports:
    """8个仿真器导入测试"""

    SIM_MODULES = [
        "bsd_sim.standing_wave_sim",
        "bsd_sim.phase_transition_sim",
        "bsd_sim.emergence_sim",
        "bsd_sim.four_force_sim",
        "bsd_sim.chemistry_sim",
        "bsd_sim.life_steady_sim",
        "bsd_sim.civilization_sim",
        "bsd_sim.cosmology_sim",
    ]

    def test_all_8_simulators_importable(self):
        """8个仿真器全部可导入"""
        for mod_name in self.SIM_MODULES:
            try:
                importlib.import_module(mod_name)
            except Exception as e:
                pytest.fail(f"仿真器 {mod_name} 导入失败: {e}")

    def test_all_simulators_have_run_method(self):
        """所有仿真器类都有run方法"""
        class_names = [
            ("bsd_sim.standing_wave_sim", "StandingWaveSimulator"),
            ("bsd_sim.phase_transition_sim", "PhaseTransitionSimulator"),
            ("bsd_sim.emergence_sim", "EmergenceSimulator"),
            ("bsd_sim.four_force_sim", "FourForceSimulator"),
            ("bsd_sim.chemistry_sim", "ChemistrySimulator"),
            ("bsd_sim.life_steady_sim", "LifeSteadySimulator"),
            ("bsd_sim.civilization_sim", "CivilizationSimulator"),
            ("bsd_sim.cosmology_sim", "CosmologySimulator"),
        ]
        for mod_name, cls_name in class_names:
            mod = importlib.import_module(mod_name)
            assert hasattr(mod, cls_name), f"{mod_name} 缺少类 {cls_name}"
            cls = getattr(mod, cls_name)
            assert hasattr(cls, "run"), f"{cls_name} 缺少 run 方法"
            assert hasattr(cls, "get_results"), f"{cls_name} 缺少 get_results 方法"

    def test_simulator_bsd_headers(self):
        """所有仿真器文件有BSD标注头"""
        sim_dir = os.path.join(PROJECT_ROOT, "bsd_sim")
        for f in os.listdir(sim_dir):
            if f.endswith(".py") and f != "__init__.py":
                with open(os.path.join(sim_dir, f), "r", encoding="utf-8") as fp:
                    content = fp.read()
                assert "归属基底" in content, f"{f} 缺少BSD标注头"


class TestStandingWaveSim:
    """驻波仿真器功能测试"""

    def test_standing_wave_runs(self):
        """驻波仿真器可运行"""
        from bsd_sim.standing_wave_sim import StandingWaveSimulator
        sim = StandingWaveSimulator(num_points=50, time_steps=100)
        sim.setup_wave(mode_n=1, kappa=0.35)
        sim.run()
        results = sim.get_results()
        assert results is not None

    def test_standing_wave_results_has_wave(self):
        """驻波仿真结果包含波形数据"""
        from bsd_sim.standing_wave_sim import StandingWaveSimulator
        sim = StandingWaveSimulator(num_points=50, time_steps=100)
        sim.setup_wave(mode_n=1, kappa=0.35)
        sim.run()
        results = sim.get_results()
        # 检查至少有某种波形输出
        has_wave = any("wave" in k.lower() or "amplitude" in k.lower() or "psi" in k.lower()
                       for k in results.keys())
        assert has_wave, f"结果中缺少波形数据: {list(results.keys())}"


class TestPhaseTransitionSim:
    """相变仿真器功能测试"""

    def test_phase_transition_runs(self):
        """相变仿真器可运行"""
        from bsd_sim.phase_transition_sim import PhaseTransitionSimulator
        sim = PhaseTransitionSimulator(T_range=(0.01, 2.0), T_steps=50)
        sim.setup_lagrangian({"a": 1.0, "b": 1.0, "Tc": 0.65})
        sim.run()
        results = sim.get_results()
        assert results is not None


class TestEmergenceSim:
    """涌现仿真器功能测试"""

    def test_emergence_runs(self):
        """涌现仿真器可运行"""
        from bsd_sim.emergence_sim import EmergenceSimulator
        sim = EmergenceSimulator(num_components=20, time_steps=100)
        sim.setup_interactions(coupling_matrix=None)
        sim.run()
        results = sim.get_results()
        assert results is not None


class TestFourForceSim:
    """四力仿真器功能测试"""

    def test_four_force_runs(self):
        """四力仿真器可运行"""
        from bsd_sim.four_force_sim import FourForceSimulator
        sim = FourForceSimulator(energy_range=(1, 1e15))
        sim.setup_running_couplings()
        sim.run()
        results = sim.get_results()
        assert results is not None


class TestChemistrySim:
    """化学仿真器功能测试"""

    def test_chemistry_runs(self):
        """化学仿真器可运行"""
        from bsd_sim.chemistry_sim import ChemistrySimulator
        sim = ChemistrySimulator(num_elements=10, time_steps=50)
        sim.setup_elements(element_params=None)
        sim.run()
        results = sim.get_results()
        assert results is not None


class TestLifeSteadySim:
    """生命稳态仿真器功能测试"""

    def test_life_steady_runs(self):
        """生命稳态仿真器可运行"""
        from bsd_sim.life_steady_sim import LifeSteadySimulator
        sim = LifeSteadySimulator(time_steps=100, dt=0.01)
        sim.setup_subject(qi=0.7, blood=0.8, body=0.75, mind=0.65, dao=0.6)
        sim.run()
        results = sim.get_results()
        assert results is not None


class TestCivilizationSim:
    """文明演化仿真器功能测试"""

    def test_civilization_runs(self):
        """文明演化仿真器可运行"""
        from bsd_sim.civilization_sim import CivilizationSimulator
        sim = CivilizationSimulator(time_steps=200, dt=0.1)
        sim.setup_civilization(six_systems_params=None)
        sim.run()
        results = sim.get_results()
        assert results is not None


class TestCosmologySim:
    """宇宙学仿真器功能测试"""

    def test_cosmology_runs(self):
        """宇宙学仿真器可运行"""
        from bsd_sim.cosmology_sim import CosmologySimulator
        sim = CosmologySimulator(time_steps=50)
        sim.setup_universe(Lambda=1.106e-52, Omega_m=0.31, Omega_r=5e-5)
        sim.run()
        results = sim.get_results()
        assert results is not None


class TestVisualizationModules:
    """4个可视化模块测试"""

    def test_wave_plots_importable(self):
        """驻波可视化模块可导入"""
        from bsd_sim.visualization import wave_plots
        assert hasattr(wave_plots, "plot_standing_wave_snapshot")
        assert hasattr(wave_plots, "plot_standing_wave_evolution")

    def test_phase_emergence_plots_importable(self):
        """相变涌现可视化模块可导入"""
        from bsd_sim.visualization import phase_emergence_plots
        assert hasattr(phase_emergence_plots, "plot_phase_diagram")
        assert hasattr(phase_emergence_plots, "plot_emergence_dynamics")

    def test_entropy_civilization_plots_importable(self):
        """熵流文明可视化模块可导入"""
        from bsd_sim.visualization import entropy_civilization_plots
        assert hasattr(entropy_civilization_plots, "plot_entropy_flow")
        assert hasattr(entropy_civilization_plots, "plot_six_systems_radar")

    def test_life_cosmology_plots_importable(self):
        """生命宇宙可视化模块可导入"""
        from bsd_sim.visualization import life_cosmology_plots
        assert hasattr(life_cosmology_plots, "plot_five_dim_steady_state")
        assert hasattr(life_cosmology_plots, "plot_cosmology_evolution")

    def test_visualization_files_have_bsd_header(self):
        """可视化文件有BSD标注"""
        vis_dir = os.path.join(PROJECT_ROOT, "bsd_sim", "visualization")
        for f in os.listdir(vis_dir):
            if f.endswith(".py") and f != "__init__.py":
                with open(os.path.join(vis_dir, f), "r", encoding="utf-8") as fp:
                    content = fp.read()
                assert "归属基底" in content, f"{f} 缺少BSD标注头"

    def test_plot_functions_return_fig(self):
        """绘图函数返回matplotlib Figure对象"""
        from bsd_sim.visualization.wave_plots import plot_standing_wave_snapshot
        wave_data = np.random.randn(10, 50)
        fig = plot_standing_wave_snapshot(wave_data)
        assert fig is not None
        plt_close(fig)

    def test_plot_entropy_flow(self):
        """熵流绘图函数正常工作"""
        from bsd_sim.visualization.entropy_civilization_plots import plot_entropy_flow
        t = np.linspace(0, 100, 200)
        e_res = 0.3 + 0.1 * np.sin(t / 10)
        fig = plot_entropy_flow(t, e_res)
        assert fig is not None
        plt_close(fig)

    def test_plot_lambda_verification(self):
        """Λ验证绘图函数正常工作"""
        from bsd_sim.visualization.life_cosmology_plots import plot_lambda_verification
        fig = plot_lambda_verification(1.106e-52, 1.109e-52, 0.27)
        assert fig is not None
        plt_close(fig)


def plt_close(fig):
    """安全关闭figure"""
    import matplotlib.pyplot as plt
    plt.close(fig)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
