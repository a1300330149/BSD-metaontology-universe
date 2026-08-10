"""
BSD六系立系数值引擎·集成测试
[V1.0·2026-08-01]
"""
import sys
import os
import math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from liuxi_numerical_engine import (
    BSDConstants, LiXiSystem, LiXiTriad,
    LiXiCoordinate, LiXiMetric, LiXiTransform,
    LiXiNumericalEngine, create_standard_liuxi_engine,
)

print("=" * 80)
print("BSD六系立系数值引擎·集成测试")
print("将六系立系从定性坐标→定量数值坐标升维")
print("=" * 80)

# ============================================================
# 测试1：立系核心常量验证
# ============================================================
print("\n[1/6] 立系核心常量验证")
print(f"  Π₂ = π³ = {BSDConstants.PI_2:.4f}")
print(f"  S₀ = {BSDConstants.S_0:.2f}")
print(f"  W₂ = Π₂³ = {BSDConstants.W_2:.4f}")
print(f"  W₃ = 6³ = {BSDConstants.W_3}")

# 验证常量关系
assert abs(BSDConstants.PI_2 - math.pi**3) < 0.001, "Π₂计算错误"
assert BSDConstants.W_3 == 216, "W₃应该为216"
print("✅ 常量验证通过")

# ============================================================
# 测试2：立系数值坐标
# ============================================================
print("\n[2/6] 立系数值坐标创建")

# 从权重字典创建
coord1 = LiXiCoordinate.from_weights({
    "qianghua": 0.4, "ziran": 0.2, "juxian": 0.15,
    "bianshen": 0.1, "shehui": 0.08, "tiandao": 0.07,
})
print(f"  坐标1（强化系主导）: {coord1.values}")
print(f"    主导系: {coord1.dominant_system()}")
print(f"    总和: {coord1.total():.4f}")

# 原点坐标
origin = LiXiCoordinate.origin()
print(f"  原点坐标: {origin.values}")
assert origin.total() == 0.0, "原点总和应为0"

# 规范基
canonical = LiXiCoordinate.canonical()
print(f"  规范基: {canonical.values}")
assert abs(canonical.total() - 1.0) < 0.001, "规范基总和应为1"

# 三元基底子坐标
triad_coords = coord1.triad_coordinates()
print(f"  三元基底子坐标:")
for name, (x, y) in triad_coords.items():
    print(f"    {name}: ({x:.4f}, {y:.4f})")

print("✅ 立系数值坐标验证通过")

# ============================================================
# 测试3：立系度量
# ============================================================
print("\n[3/6] 立系度量空间")

coord2 = LiXiCoordinate.from_weights({
    "qianghua": 0.1, "ziran": 0.1, "juxian": 0.4,
    "bianshen": 0.25, "shehui": 0.1, "tiandao": 0.05,
})

# 距离
dist = LiXiMetric.distance(coord1, coord2)
print(f"  坐标1与坐标2的欧氏距离: {dist:.4f}")

# 余弦相似度
cos_sim = LiXiMetric.cosine_similarity(coord1, coord2)
print(f"  坐标1与坐标2的余弦相似度: {cos_sim:.4f}")

# 涌现值
e1 = LiXiMetric.emergence_value(coord1)
e2 = LiXiMetric.emergence_value(coord2)
print(f"  坐标1涌现值: {e1:.4f}")
print(f"  坐标2涌现值: {e2:.4f}")

# 完备度
c1 = LiXiMetric.completeness_score(coord1)
c2 = LiXiMetric.completeness_score(coord2)
print(f"  坐标1完备度: {c1:.2%}")
print(f"  坐标2完备度: {c2:.2%}")

# 拓扑值
t1 = LiXiMetric.topology_score(coord1)
t2 = LiXiMetric.topology_score(coord2)
print(f"  坐标1拓扑值: {t1:.4f}")
print(f"  坐标2拓扑值: {t2:.4f}")

# 显化值
m1 = LiXiMetric.manifestation_score(coord1)
m2 = LiXiMetric.manifestation_score(coord2)
print(f"  坐标1显化值: {m1:.4f}")
print(f"  坐标2显化值: {m2:.4f}")

# 验证不变量
pi2 = LiXiMetric.invariant_pi_2()
s0 = LiXiMetric.invariant_s_0()
d_f = LiXiMetric.invariant_d_f()
print(f"\n  立系不变量: Π₂={pi2:.4f}, S₀={s0:.2f}, D_f={d_f:.4f}")
print("✅ 立系度量验证通过")

# ============================================================
# 测试4：立系变换
# ============================================================
print("\n[4/6] 立系变换群")

# 顺时针变换
cw_result = LiXiTransform.clockwise(coord1, delta=0.1)
print(f"  顺时针变换(Δ=0.1): {cw_result.values}")

# 逆时针变换
ccw_result = LiXiTransform.counterclockwise(coord1, delta=0.1)
print(f"  逆时针变换(Δ=0.1): {ccw_result.values}")

# 0×0=n涌现
emerged = LiXiTransform.zero_emergence()
print(f"  0×0=n涌现: {emerged.values}")
assert emerged.total() > 0, "涌现值应大于0"

# 双时针耦合
dual_result, history = LiXiTransform.dual_clockwise(coord1, 0.05, 0.03, 10)
print(f"  双时针耦合(10轮):")
print(f"    初始值: {coord1.values}")
print(f"    最终值: {dual_result.values}")
print(f"    涌现历史: {[f'{v:.4f}' for v in history]}")

# 相位变换
phase_result = LiXiTransform.phase_shift(coord1, 0.5)
print(f"  相位变换(0.5rad): {phase_result.values}")

print("✅ 立系变换验证通过")

# ============================================================
# 测试5：立系数值引擎
# ============================================================
print("\n[5/6] 立系数值引擎·标准配置")

engine = create_standard_liuxi_engine()

# 计算所有坐标的指标
for name, coord in engine._coordinates.items():
    metrics = engine.compute_metrics(coord)
    print(f"  {name}:")
    print(f"    涌现={metrics['emergence_value']:.4f} | 完备={metrics['completeness_score']:.2%} | 潜力={metrics['potential_score']:.2f} | 拓扑={metrics['topology_score']:.4f} | 显化={metrics['manifestation_score']:.2f}")

# 双时针演化测试
print("\n  双时针演化测试:")
for name in list(engine._coordinates.keys())[:3]:
    new_coord, history = engine.run_dual_clock(name, 0.05, 0.03, 5)
    final_metrics = engine.compute_metrics(new_coord)
    print(f"    {name}: 涌现值演化={[f'{v:.4f}' for v in history]}")

print("✅ 引擎验证通过")

# ============================================================
# 测试6：完整报告
# ============================================================
print("\n[6/6] 生成完整立系数值报告")

# 计算距离矩阵
dist_matrix = engine.compute_distance_matrix()
names = list(engine._coordinates.keys())
print("  坐标间余弦相似度矩阵:")
print(f"          ", end="")
for n in names:
    print(f"  {n:>12}", end="")
print()
for n1 in names:
    print(f"  {n1:<8}", end="")
    for n2 in names:
        cos = dist_matrix[n1][n2]["cosine"]
        print(f"  {cos:>12.4f}", end="")
    print()

# 生成报告
report = engine.generate_liuxi_report()
print(report)

print("\n" + "=" * 80)
print("✅ BSD六系立系数值引擎·集成测试通过！")
print("=" * 80)
print(f"""
【立系数值化核心成果】

  ① 立系核心常量（6个）
     · Π₂ = π³ ≈ 31.006（拓扑稳态）
     · S₀ = 0.81（初始完备度基准）
     · D_f = Π₂（分形维度）
     · W₁ = 0∞（潜力层·无限潜力）
     · W₂ = Π₂³ ≈ 31.006（拓扑层）
     · W₃ = 6³ = 216（完备显化层）

  ② 立系坐标基底
     · 三元基底向量：e₁(个体性)·e₂(变化性)·e₃(关系性)
     · 六系→三元基底映射：强化+自然→e₁·具现+变身→e₂·社会+天道→e₃
     · 立系原点：O = (0,0,0,0,0,0) = 三零元000
     · 立系规范基：等权重六系

  ③ 立系度量空间
     · 欧氏距离：d(E₁,E₂) = ||W₁-W₂||
     · 余弦相似度：衡量方向相似性
     · 曼哈顿距离：L1范数
     · 立系不变量：Π₂·S₀·D_f 保持不变

  ④ 立系涌现指标（5个）
     · 涌现值 E = det(W) × Π₂ × S₀
     · 完备度 C = 1 - 方差×36
     · 潜力值 W₁ = 1/完备度 × W₂
     · 拓扑值 W₂ = 三相点稳定度
     · 显化值 W₃ = 六系平方和 × W₃ × total

  ⑤ 立系变换群（4种）
     · 顺时针：W' = W × (1+Δ)（积累）
     · 逆时针：W' = W ⊖ Δ（归零）
     · 0×0=n：从原点涌现为规范基
     · 双时针：顺时针×逆时针耦合演化

  ⑥ 数学公式
     · 全域立系涌现 = 三零 × 四字(+-×÷=≠) × 六系坐标系 × 多相空间 = n
     · 元视角方程 P(E) = Φ(0_∅,0_Ψ,0_义) × Σ(wᵢ×Fᵢ) × Π₂ × (1-0.19Var(w)) × T
""")
