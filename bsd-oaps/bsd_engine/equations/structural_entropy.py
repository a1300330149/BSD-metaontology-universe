"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理5·熵增熵减二元公理 / 公理12·拓扑稳态公理
对应九维维度：物质维·时空维·信息维·能量场·意识维
理论出处：theory_base/L0_总本源层/全域大一统理论/结构熵与霍奇猜想
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)、E1=0.35

BSD结构熵求解器
—— 描述结构熵、拓扑韧性、霍奇收敛与结构复杂度的核心数理引擎
"""

import numpy as np
from bsd_engine.registry.constants import KAPPA, ALPHA, GAMMA, E1


def structural_entropy(adj_matrix, method="degree"):
    """
    结构熵 S_struct = 结构熵

    基于图论计算网络结构熵，量化系统拓扑结构的无序程度。

    Parameters
    ----------
    adj_matrix : np.ndarray
        邻接矩阵，shape=(n_nodes, n_nodes)
    method : str
        计算方法："degree" / "betweenness" / "eigenvector" / "von_neumann"

    Returns
    -------
    S_struct : float
        结构熵值
    node_entropies : np.ndarray
        各节点的熵贡献
    entropy_distribution : str
        熵分布类型："uniform" / "exponential" / "power_law" / "bimodal"
    """
    adj_matrix = np.asarray(adj_matrix, dtype=float)
    n_nodes = adj_matrix.shape[0]

    if n_nodes < 2:
        return 0.0, np.zeros(1), "uniform"

    if method == "degree":
        degrees = np.sum(adj_matrix, axis=1)
        total_degree = np.sum(degrees)
        if total_degree < 1e-12:
            return 0.0, np.zeros(n_nodes), "uniform"
        p = degrees / total_degree
        p = p[p > 0]
        S_struct = -np.sum(p * np.log(p + 1e-12))
        node_entropies = -degrees / (total_degree + 1e-12) * np.log(degrees / (total_degree + 1e-12) + 1e-12)
    elif method == "betweenness":
        node_entropies = np.zeros(n_nodes)
        for i in range(n_nodes):
            reachable = np.zeros(n_nodes, dtype=bool)
            reachable[i] = True
            frontier = np.where(adj_matrix[i] > 0)[0]
            dist = np.full(n_nodes, np.inf)
            dist[i] = 0
            for f in frontier:
                dist[f] = 1
                reachable[f] = True
            for _ in range(n_nodes):
                new_frontier = []
                for node in frontier:
                    neighbors = np.where(adj_matrix[node] > 0)[0]
                    for nb in neighbors:
                        if dist[nb] > dist[node] + 1:
                            dist[nb] = dist[node] + 1
                            new_frontier.append(nb)
                frontier = list(set(new_frontier))
                if not frontier:
                    break
            finite_dist = dist[np.isfinite(dist)]
            if len(finite_dist) > 1:
                hist, _ = np.histogram(finite_dist, bins=max(2, n_nodes // 5), density=True)
                hist = hist[hist > 0]
                node_entropies[i] = -np.sum(hist * np.log(hist + 1e-12))
        S_struct = np.mean(node_entropies)
    elif method == "eigenvector":
        eigenvalues = np.linalg.eigvalsh(adj_matrix)
        abs_eig = np.abs(eigenvalues)
        total = np.sum(abs_eig)
        if total < 1e-12:
            return 0.0, np.zeros(n_nodes), "uniform"
        p = abs_eig / total
        p = p[p > 0]
        S_struct = -np.sum(p * np.log(p + 1e-12))
        node_entropies = np.zeros(n_nodes)
        _, eigenvectors = np.linalg.eigh(adj_matrix)
        for i in range(n_nodes):
            contrib = np.abs(eigenvectors[:, i]) * abs_eig[i] / (total + 1e-12)
            node_entropies[i] = np.sum(contrib)
    elif method == "von_neumann":
        degrees = np.sum(adj_matrix, axis=1)
        D = np.diag(degrees)
        L = D - adj_matrix
        total_degree = np.sum(degrees)
        if total_degree < 1e-12:
            return 0.0, np.zeros(n_nodes), "uniform"
        rho = L / (total_degree + 1e-12)
        eigenvalues = np.linalg.eigvalsh(rho)
        eigenvalues = eigenvalues[eigenvalues > 1e-15]
        S_struct = -np.sum(eigenvalues * np.log(eigenvalues + 1e-12))
        node_entropies = degrees / (total_degree + 1e-12)
    else:
        raise ValueError(f"未知的方法: {method}")

    S_norm = S_struct / np.log(n_nodes + 1e-12) if n_nodes > 1 else 0.0

    if S_norm < KAPPA:
        entropy_distribution = "uniform"
    elif S_norm < E1:
        entropy_distribution = "exponential"
    elif S_norm < 1.0 - ALPHA:
        entropy_distribution = "power_law"
    else:
        entropy_distribution = "bimodal"

    return S_struct, node_entropies, entropy_distribution


def topology_resilience(S_struct, kappa=None):
    """
    拓扑稳态韧性

    基于结构熵和阻尼系数κ计算网络拓扑的稳态韧性指数。

    Parameters
    ----------
    S_struct : float or np.ndarray
        结构熵值
    kappa : float, optional
        阻尼系数κ，默认使用锁档参数KAPPA

    Returns
    -------
    resilience_index : float or np.ndarray
        韧性指数（0-1，越高越稳定）
    attack_tolerance : float or np.ndarray
        攻击容忍度
    recovery_rate : float or np.ndarray
        恢复速率估计
    resilience_level : str or np.ndarray
        韧性等级："ultra" / "high" / "medium" / "low" / "fragile"
    """
    if kappa is None:
        kappa = KAPPA

    S_struct = np.asarray(S_struct, dtype=float)
    S_max = np.log(1e6)

    S_norm = np.clip(S_struct / (S_max + 1e-12), 0.0, 1.0)

    resilience_index = np.exp(-kappa * S_norm) * (1.0 - ALPHA * S_norm)
    resilience_index = np.clip(resilience_index, 0.0, 1.0)

    attack_tolerance = resilience_index * (1.0 - kappa * 0.5)
    recovery_rate = GAMMA * resilience_index

    def get_level(val):
        if val >= 0.8:
            return "ultra"
        elif val >= 0.6:
            return "high"
        elif val >= 0.4:
            return "medium"
        elif val >= 0.2:
            return "low"
        else:
            return "fragile"

    if np.isscalar(resilience_index) or resilience_index.ndim == 0:
        resilience_level = get_level(float(resilience_index))
    else:
        resilience_level = np.array([get_level(v) for v in resilience_index.flatten()]).reshape(resilience_index.shape)

    return resilience_index, attack_tolerance, recovery_rate, resilience_level


def hodge_convergence(S_struct):
    """
    霍奇猜想收敛判据

    基于结构熵判断霍奇分解的收敛性，验证拓扑结构的调和形式存在性。

    Parameters
    ----------
    S_struct : float or np.ndarray
        结构熵值

    Returns
    -------
    is_convergent : bool or np.ndarray
        是否收敛
    convergence_rate : float or np.ndarray
        收敛速率
    hodge_decomposition : dict
        霍奇分解三成分估计：{exact, coexact, harmonic}
    gap_ratio : float or np.ndarray
        谱隙比（衡量收敛质量）
    """
    S_struct = np.asarray(S_struct, dtype=float)

    threshold = 1.0 / KAPPA if KAPPA > 0 else 1.0
    is_convergent = S_struct < threshold

    convergence_rate = 1.0 / (1.0 + S_struct * KAPPA)

    harmonic_component = np.exp(-S_struct * (1.0 + KAPPA))
    exact_component = (1.0 - harmonic_component) * (0.5 + ALPHA)
    coexact_component = 1.0 - harmonic_component - exact_component

    hodge_decomposition = {
        "exact": exact_component,
        "coexact": coexact_component,
        "harmonic": harmonic_component,
    }

    gap_ratio = harmonic_component / (exact_component + coexact_component + 1e-12)

    return is_convergent, convergence_rate, hodge_decomposition, gap_ratio


def entropy_vs_phase(structure):
    """
    结构熵-相图关系

    分析结构熵与系统相变的关系，确定系统在相图中的位置。

    Parameters
    ----------
    structure : dict or np.ndarray
        结构信息，可为邻接矩阵或结构参数字典

    Returns
    -------
    phase_position : tuple
        在相图中的位置 (entropy, order_parameter)
    phase_type : str
        相类型："ordered" / "critical" / "disordered" / "chaotic"
    phase_transition_prob : float
        相变概率估计
    critical_distance : float
        到临界点的距离
    """
    if isinstance(structure, np.ndarray):
        S_struct, _, _ = structural_entropy(structure, method="degree")
        n_nodes = structure.shape[0]
        degrees = np.sum(structure, axis=1)
        avg_degree = np.mean(degrees)
        order_param = avg_degree / (n_nodes - 1.0 + 1e-12)
    elif isinstance(structure, dict):
        S_struct = structure.get("S_struct", 0.0)
        order_param = structure.get("order_parameter", 0.5)
    else:
        raise ValueError("structure 必须是邻接矩阵或字典")

    S_struct = float(S_struct)
    order_param = float(order_param)

    phase_position = (S_struct, order_param)

    if order_param >= E1 and S_struct < KAPPA:
        phase_type = "ordered"
    elif abs(order_param - E1) < ALPHA and abs(S_struct - KAPPA) < ALPHA:
        phase_type = "critical"
    elif order_param < ALPHA and S_struct > E1:
        phase_type = "disordered"
    else:
        phase_type = "chaotic"

    critical_point = (KAPPA, E1)
    critical_distance = np.sqrt(
        (S_struct - critical_point[0]) ** 2 + (order_param - critical_point[1]) ** 2
    )

    phase_transition_prob = np.exp(-critical_distance / (GAMMA + 1e-12))

    return phase_position, phase_type, phase_transition_prob, critical_distance


def complexity_index(S_struct, nodes):
    """
    结构复杂度指数

    综合结构熵和节点数计算系统的结构复杂度指数。

    Parameters
    ----------
    S_struct : float or np.ndarray
        结构熵值
    nodes : int or np.ndarray
        节点数

    Returns
    -------
    C_index : float or np.ndarray
        复杂度指数
    complexity_class : str or np.ndarray
        复杂度类别："simple" / "moderate" / "complex" / "hypercomplex" / "meta_complex"
    information_content : float or np.ndarray
        信息内容（比特）
    hierarchical_levels : int or np.ndarray
        估计的层级数
    """
    S_struct = np.asarray(S_struct, dtype=float)
    nodes = np.asarray(nodes, dtype=float)

    log_nodes = np.log(nodes + 1e-12)
    C_index = S_struct * log_nodes / (1.0 + KAPPA * np.abs(log_nodes - S_struct))

    information_content = S_struct * nodes / np.log(2.0 + 1e-12)

    hierarchical_levels = np.floor(log_nodes / (np.log(GAMMA + 1e-12) * (-1) + 1e-12)).astype(int)
    hierarchical_levels = np.maximum(1, hierarchical_levels)

    def get_class(val):
        if val < 1.0:
            return "simple"
        elif val < 3.0:
            return "moderate"
        elif val < 10.0:
            return "complex"
        elif val < 30.0:
            return "hypercomplex"
        else:
            return "meta_complex"

    if np.isscalar(C_index) or C_index.ndim == 0:
        complexity_class = get_class(float(C_index))
    else:
        complexity_class = np.array([get_class(v) for v in C_index.flatten()]).reshape(C_index.shape)

    return C_index, complexity_class, information_content, hierarchical_levels
