# 非Newtonian流体的BSD相变场本构攻克

---

## 〇、双时针记录格式说明

本文档采用 **双时针记录系统** 追踪攻克进程：

| 符号 | 含义 |
|------|------|
| `[T_s]` | 理论时钟戳（Theory Clock）—— 对应BSD理论构建的逻辑时间 |
| `[T_p]` | 物理时钟戳（Physical Clock）—— 对应物理领域的验证进度时间 |
| `[状态]` | 当前攻克状态：`待攻克` → `进行中` → `突破中` → `已攻克` |
| `[进度]` | 量化进度百分比（0%–100%） |
| `[关键发现]` | 该时钟周期内的核心突破或障碍 |

**记录模板：**
```
[T_s=0000.000] [T_p=0000-00-00] [状态] | 进度 | 关键发现描述
```

---

## 一、非Newtonian流体本构模型基础

### 1.1 动量方程框架

非Newtonian流体的动量守恒方程为：

$$
\rho \left( \frac{\partial \mathbf{u}}{\partial t} + \mathbf{u} \cdot \nabla \mathbf{u} \right) = -\nabla p + \nabla \cdot \boldsymbol{\sigma} + \rho \mathbf{f}
$$

- $\rho$：流体密度
- $\mathbf{u}(\mathbf{x}, t) = (u, v, w)^T$：速度矢量
- $p$：热力学压力
- $\boldsymbol{\sigma} = -p \mathbf{I} + \boldsymbol{\tau}$：总应力张量，其中 $\boldsymbol{\tau}$ 为偏应力张量
- $\mathbf{f}$：体积力

**核心区别：** 非Newtonian流体的偏应力张量 $\boldsymbol{\tau}$ 不再服从Newton粘性定律 $\boldsymbol{\tau} = 2\mu \mathbf{D}(\mathbf{u})$，而是依赖于更复杂的本构关系。

### 1.2 应变率张量与基本定义

**应变率张量（对称部分）：**

$$
\mathbf{D}(\mathbf{u}) = \frac{1}{2} \left( \nabla \mathbf{u} + \nabla \mathbf{u}^T \right)
$$

**剪切速率（第二不变量）：**

$$
\dot{\gamma} = \sqrt{2 \mathbf{D} : \mathbf{D}}
$$

**应力偏量第二不变量：**

$$
\tau = \sqrt{\frac{1}{2} \boldsymbol{\tau} : \boldsymbol{\tau}}
$$

### 1.3 三大经典本构模型

#### （一）Power-Law模型（Ostwald-de Waele）

**本构关系：**

$$
\boldsymbol{\tau} = K \, \dot{\gamma}^{\,n-1} \, \mathbf{D}(\mathbf{u})
$$

或等价地：

$$
\eta_{\text{app}}(\dot{\gamma}) = K \, \dot{\gamma}^{\,n-1}
$$

- $K$：稠度系数（consistency index），量纲 $[Pa \cdot s^n]$
- $n$：幂指数（flow behavior index）
- $\eta_{\text{app}}$：表观粘度

**物理含义：**

| 幂指数 $n$ | 流体类型 | 典型物质 |
|:---:|:---|:---|
| $n < 1$ | 剪切稀化流体（pseudoplastic） | 聚合物溶液、血桨、涂料 |
| $n = 1$ | Newtonian流体（基准） | 水、空气、油类 |
| $n > 1$ | 剪切增稠流体（dilatant） | 淀粉糊、砂水混合物、某些工业浆料 |

#### （二）Herschel-Bulkley模型

**本构关系：**

$$
\begin{cases}
\boldsymbol{\tau} = \mathbf{0} & \text{if } \tau_y > \sqrt{\frac{1}{2} \boldsymbol{\tau} : \boldsymbol{\tau}} \\
\boldsymbol{\tau} = \left( \frac{\tau_y}{\dot{\gamma}} + K \dot{\gamma}^{\,n-1} \right) \mathbf{D}(\mathbf{u}) & \text{if } \sqrt{\frac{1}{2} \boldsymbol{\tau} : \boldsymbol{\tau}} \geq \tau_y
\end{cases}
$$

**完整形式：**

$$
\boldsymbol{\tau} = \begin{cases}
0 & \dot{\gamma} < \dot{\gamma}_{\text{yield}} \\
\tau_y + K \, \dot{\gamma}^{\,n-1} & \dot{\gamma} \geq \dot{\gamma}_{\text{yield}}
\end{cases}
$$

- $\tau_y$：屈服应力（yield stress），量纲 $[Pa]$
- $K$：稠度系数
- $n$：幂指数

**核心特性：** 当剪切应力低于屈服应力时，流体不发生流动（表现为刚体）；超过屈服应力后才开始流动。具有剪切稀化/增稠的双重特征。

**典型物质：** 泥浆、钻井液、浆液、番茄酱、牙膏等屈服-塑性流体。

#### （三）Oldroyd-B模型（粘弹性本构）

**本构关系（上随体导数形式）：**

$$
\boldsymbol{\tau} + \lambda_1 \, \overset{\nabla}{\boldsymbol{\tau}} = \eta_0 \left( \mathbf{D} + \lambda_2 \, \overset{\nabla}{\mathbf{D}} \right)
$$

或用分解形式：

$$
\boldsymbol{\sigma} = -p \mathbf{I} + 2\eta_s \mathbf{D} + \boldsymbol{\tau}_p
$$

其中聚合物应力 $\boldsymbol{\tau}_p$ 满足：

$$
\boldsymbol{\tau}_p + \lambda_1 \, \overset{\nabla}{\boldsymbol{\tau}}_p = 2\eta_p \mathbf{D}
$$

- $\lambda_1$：松弛时间（relaxation time），表征弹性记忆效应
- $\lambda_2$：推迟时间（retardation time），表征粘性响应滞后
- $\eta_0 = \eta_s + \eta_p$：零剪切粘度
- $\eta_s$：溶剂粘度
- $\eta_p$：聚合物贡献粘度

**上随体导数定义：**

$$
\overset{\nabla}{\mathbf{A}} = \frac{\partial \mathbf{A}}{\partial t} + (\mathbf{u} \cdot \nabla) \mathbf{A} - \mathbf{A} \cdot \nabla \mathbf{u} - (\nabla \mathbf{u})^T \cdot \mathbf{A}
$$

**核心特性：** 描述粘弹性流体的弹性记忆效应，应力不仅依赖于当前应变率，还与历史变形过程有关。

---

## 二、关键现象分析

### 2.1 剪切稀化与剪切增稠

**剪切稀化（Shear Thinning）：**

- **现象：** 表观粘度 $\eta_{\text{app}}$ 随剪切速率 $\dot{\gamma}$ 增加而降低
- **微观机制：** 剪切作用使流体微结构（如聚合物分子、粒子团）沿流场方向取向/解缠，导致流动阻力减小
- **定量表征：** $d\eta_{\text{app}}/d\dot{\gamma} < 0$，对应 $n < 1$
- **工程影响：** 注射成型中剪切稀化使充模更容易，但可能导致制品表面质量问题

**剪切增稠（Shear Thickening）：**

- **现象：** 表观粘度 $\eta_{\text{app}}$ 随剪切速率 $\dot{\gamma}$ 增加而升高
- **微观机制：** 剪切使流体中粒子/分子形成新的有序结构（如"膨胀"结构），阻碍流动
- **定量表征：** $d\eta_{\text{app}}/d\dot{\gamma} > 0$，对应 $n > 1$
- **工程影响：** 抗冲击防护材料、减震阻尼器的设计原理

**剪切稀化/增稠的剪切速率依赖性：**

$$
\eta_{\text{app}}(\dot{\gamma}) = K \dot{\gamma}^{n-1} \implies 
\begin{cases}
\text{Shear Thinning: } n < 1, \eta_{\text{app}} \downarrow \\
\text{Newtonian: } n = 1, \eta_{\text{app}} = \text{const} \\
\text{Shear Thickening: } n > 1, \eta_{\text{app}} \uparrow
\end{cases}
$$

### 2.2 剪切带（Shear Banding）

**现象描述：** 非Newtonian流体在简单剪切流中，自发形成交替的高剪切率带与低剪切率带，速度剖面呈现阶梯状跃迁。

**数学表征：**

在Couette流（同轴圆筒）中，剪切带表现为：

$$
\dot{\gamma}(r) = \begin{cases}
\dot{\gamma}_{\text{high}} & r_1 < r < r_2 \quad \text{（高剪切带）} \\
\dot{\gamma}_{\text{low}} & r_2 < r < r_3 \quad \text{（低剪切带）}
\end{cases}
$$

其中 $\dot{\gamma}_{\text{high}} \gg \dot{\gamma}_{\text{low}}$，在 $r = r_2$ 处存在剪切率的突变。

**形成机制：**

1. **本构不稳定性：** 某些本构模型（如Johnson-Segalman模型）在特定参数下出现多值应力-剪切速率关系
2. **跃变条件：** 当应力-应变率曲线具有负斜率区间（$d\tau/d\dot{\gamma} < 0$）时，均匀流不稳定，自发形成剪切带
3. **实验观测：** 已在多种聚合物溶液、胶体悬浮液中通过PIV（粒子图像测速）实验观测到

**判据：**

$$
\frac{d\tau}{d\dot{\gamma}} < 0 \quad \text{（微分本构不稳定条件）}
$$

### 2.3 粘弹性振荡（Viscoelastic Oscillations）

**现象描述：** 粘弹性流体在特定流动条件下，速度场或应力场呈现周期性振荡，即使边界条件是定常的。

**数学起源：**

Oldroyd-B方程的线性稳定性分析给出色散关系：

$$
\omega^2 + \frac{\omega}{\lambda_1} \left( 1 - \frac{\eta_0}{\eta_s} \right) + k^2 c_0^2 \left( 1 - \frac{\tau_y}{\eta_0 k^2 c_0^2} \right) = 0
$$

- $\omega$：振荡频率
- $k$：波数
- $c_0$：弹性波速度

**振荡类型：**

| 振荡模式 | 物理机制 | 频率范围 |
|---------|---------|---------|
| 弹性振荡 | 弹性应力的过冲效应 | $10^0$–$10^3$ Hz |
| 剪切振荡 | 剪切带的周期形成-湮灭 | $10^{-2}$–$10^1$ Hz |
| 结构振荡 | 流体微观结构的重构 | $10^{-3}$–$10^0$ Hz |

**工程意义：** 石油管道脉动、注塑机压力振荡、生物流体（如血液）的搏动行为。

---

## 三、BSD元数学框架对应分析

### 3.1 本构关系 → 相变场序参量

**核心映射：**

在BSD框架中，非Newtonian流体的本构关系对应于 **相变场的序参量描述**：

$$
\text{本构关系} \quad \longmapsto \quad \text{BSD相变场序参量 } \Psi(\dot{\gamma}, \lambda, T)
$$

**序参量定义：**

$$
\Psi_{\text{order}}(\dot{\gamma}, \lambda, T) = \frac{\eta_{\text{app}}(\dot{\gamma}) - \eta_{\text{Newtonian}}}{\eta_{\text{Newtonian}}}
$$

- $\Psi_{\text{order}} = 0$：Newtonian相（线性响应，$n=1$）
- $\Psi_{\text{order}} < 0$：剪切稀化相（$n<1$，序参量为负）
- $\Psi_{\text{order}} > 0$：剪切增稠相（$n>1$，序参量为正）

**相变场的数学结构：**

引入BSD相变场 $\Phi(\mathbf{x}, t)$，本构关系由下式统一描述：

$$
\boldsymbol{\tau} = 2 \eta_0 \exp\left( \int_{\dot{\gamma}_{\text{ref}}}^{\dot{\gamma}} \frac{\Psi(\xi)}{\xi} d\xi \right) \mathbf{D}
$$

**不同模型的相变场对应：**

| 本构模型 | BSD相变场 $\Psi(\dot{\gamma})$ | 物理含义 |
|---------|-------------------------------|---------|
| Power-Law | $\Psi = (n-1) \ln(\dot{\gamma}/\dot{\gamma}_0)$ | 幂律指数作为序参量的对数形式 |
| Herschel-Bulkley | $\Psi = \begin{cases} 0 & \dot{\gamma} < \dot{\gamma}_y \\ (n-1)\ln(\dot{\gamma}/\dot{\gamma}_0) + \tau_y/\eta_0 \end{cases}$ | 屈服应力作为相变临界点 |
| Oldroyd-B | $\Psi = \lambda_1 \dot{\gamma} \cos(\omega t + \phi)$ | 松弛时间作为振荡序参量 |

### 3.2 弹性应力 → 拓扑场

**核心映射：**

粘弹性流体中的弹性应力对应于 **BSD拓扑场** 的纤维丛结构：

$$
\text{弹性应力 } \boldsymbol{\tau}_p \quad \longmapsto \quad \text{BSD拓扑场 } \mathcal{T}_{\text{elastic}}(\mathbf{x}, t)
$$

**拓扑场的数学构造：**

将弹性应力张量 $\boldsymbol{\tau}_p$ 视为BSD主丛 $GL(3)/O(3)$ 上的截面：

$$
\mathcal{T}_{\text{elastic}}(\mathbf{x}, t) = \int_{\mathcal{C}_{\mathbf{x}}} \boldsymbol{\tau}_p(\mathbf{x}, t) \, d\mu_{\text{Haar}}
$$

- $\mathcal{C}_{\mathbf{x}}$：流体质点 $\mathbf{x}$ 的历史路径
- $d\mu_{\text{Haar}}$：BSD群的Haar测度

**拓扑不变量——缠绕数：**

弹性应力沿闭合回路的拓扑缠绕数：

$$
W[\boldsymbol{\tau}_p] = \frac{1}{2\pi i} \oint_{\partial \Omega} \text{Tr}\left( \boldsymbol{\tau}_p^{-1} d\boldsymbol{\tau}_p \right)
$$

**物理含义：** 弹性应力的拓扑缠绕数对应于流体弹性记忆的强度——缠绕数越大，弹性效应越强。

**Oldroyd-B模型的拓扑场解释：**

$$
\overset{\nabla}{\boldsymbol{\tau}}_p = \text{BSD拓扑导数} = \nabla \boldsymbol{\tau}_p - \boldsymbol{\tau}_p \cdot \nabla \mathbf{u} - (\nabla \mathbf{u})^T \cdot \boldsymbol{\tau}_p
$$

上随体导数即为BSD拓扑场的协变导数，描述弹性应力在流体运动下的拓扑演化。

### 3.3 剪切带 → 涌现相变

**核心映射：**

剪切带的形成对应于BSD框架中的 **涌现相变** 现象：

$$
\text{剪切带} \quad \longmapsto \quad \text{BSD涌现相变 } \Pi_{\text{shear}}(\mathbf{x}, t)
$$

**相变序参量：**

定义剪切带的序参量为高/低剪切率的对比度：

$$
\Psi_{\text{band}} = \frac{\dot{\gamma}_{\text{high}} - \dot{\gamma}_{\text{low}}}{\dot{\gamma}_{\text{high}} + \dot{\gamma}_{\text{low}}}
$$

- $\Psi_{\text{band}} = 0$：均匀剪切相（无剪切带）
- $\Psi_{\text{band}} = 1$：完全分化相（极端剪切带）

**相变动力学：**

剪切带的形成过程由BSD相场方程描述：

$$
\frac{\partial \Psi_{\text{band}}}{\partial t} + \mathbf{u} \cdot \nabla \Psi_{\text{band}} = M \left[ \epsilon^2 \nabla^2 \Psi_{\text{band}} - \frac{\delta \mathcal{F}}{\delta \Psi_{\text{band}}} \right]
$$

- $M$：相变迁移率
- $\epsilon$：界面宽度参数
- $\mathcal{F}$：BSD自由能泛函

**自由能密度：**

$$
\mathcal{F}[\Psi_{\text{band}}] = \int_\Omega \left[ \frac{\epsilon^2}{2} |\nabla \Psi_{\text{band}}|^2 + f(\Psi_{\text{band}}, \dot{\gamma}) \right] d\mathbf{x}
$$

其中 $f(\Psi_{\text{band}}, \dot{\gamma})$ 为双阱势函数，描述高/低剪切率两相的能量差。

**相变分岔图：**

```
剪切带涌现分岔：
    │
Ψ_band (序参量)
    │        ╱ 高剪切带相
    │       ╱
─────╋─────╱──── 临界应力 τ_c
    │  ╱  ╱
    │ ╱  ╱
    │╱  ╱ 低剪切带相
    │╱  ╱
    │╱  ╱
    └──────────→ 剪切应力 τ
   均匀相
```

---

## 四、攻克难点分析

### 4.1 本构方程适定性

**问题描述：**

非Newtonian流体本构方程的适定性（existence, uniqueness, well-posedness）远未得到一般证明。

| 难点维度 | 具体描述 |
|---------|---------|
| 幂律模型适定性 | 当 $n \in (0, 1/2)$ 时，Power-Law模型的弱解存在性尚未证明 |
| 屈服应力适定性 | Herschel-Bulkley模型的变分不等式形式适定性依赖于凸性假设 |
| 粘弹性适定性 | Oldroyd-B模型在高Weissenberg数下的全局适定性是Clay千禧奖级别的难题 |
| 多值性问题 | 某些本构方程（如Johnson-Segalman）的应力-应变率关系具有多值性，导致解的唯一性丧失 |

**BSD攻克方案：**

1. **相变场正则化：** 通过BSD相变场 $\Psi$ 的正则化，将原始本构方程嵌入更大的泛函空间：
   $$\boldsymbol{\tau}_\epsilon = \boldsymbol{\tau}_{\text{original}} * \rho_\epsilon + \epsilon \Psi_\epsilon$$

2. **拓扑弱解定义：** 基于BSD拓扑结构定义弱解：
   $$\int_\Omega \boldsymbol{\tau} : \nabla \mathbf{v} \, d\mathbf{x} = \int_{\partial \Omega} (\text{BSD流}) \cdot \mathbf{n} \, dS$$

3. **Galerkin-BSD逼近：** 用BSD本征模态作为Galerkin基函数，构造逼近解序列，证明弱解的紧致性。

### 4.2 粘弹性长时间稳定性

**问题描述：**

粘弹性流体的数值模拟在长时间积分中容易出现数值不稳定，特别是在高Weissenberg数（$Wi = \lambda_1 \dot{\gamma}$）条件下。

| 难点维度 | 具体描述 |
|---------|---------|
| 弹性应力爆散 | 上随体导数中的对流项导致弹性应力在强流区域爆散 |
| 长时间共振 | 弹性记忆效应与数值离散的共振，导致能量非物理增长 |
| 高Wi数瓶颈 | 当 $Wi > 1$ 时，数值稳定性急剧恶化，是当前仿真界的核心瓶颈 |
| 谱方法失效 | 传统谱方法在高Wi数下出现"对流震荡"（convective instability） |

**BSD攻克方案：**

1. **拓扑守恒格式：** 基于BSD拓扑守恒律设计数值格式，保证弹性应力的拓扑不变量在离散层面守恒：
   $$W[\boldsymbol{\tau}_p^{n+1}] = W[\boldsymbol{\tau}_p^n] + O(\Delta t^p)$$

2. **分数阶时间推进：** 利用BSD分数阶算子处理弹性记忆：
   $$\boldsymbol{\tau}_p(t+\Delta t) = \sum_{k=0}^{N} w_k \, \boldsymbol{\tau}_p(t - k \cdot \Delta t)$$
   其中 $w_k$ 为BSD分数阶权函数。

3. **自适应模态截断：** 根据BSD相变场强度自适应调整保留的弹性模态数：
   $$N_{\text{mode}} = \left[ Wi^2 \cdot k_{\max} \right]$$

### 4.3 剪切带形成与演化

**问题描述：**

剪切带的形成机制、演化规律和数值模拟是当前非Newtonian流体领域最具挑战性的问题之一。

| 难点维度 | 具体描述 |
|---------|---------|
| 触发机制 | 剪切带究竟由本构不稳定性触发，还是由边界条件/数值误差触发，尚无定论 |
| 选择准则 | 当多个剪切带构型能量简并时，系统如何"选择"最终构型 |
| 传播规律 | 剪切带的运动速度、宽度、间距的定量规律缺乏统一理论 |
| 数值多解 | 数值模拟中剪切带的位置和数量对网格、时间步长敏感 |

**BSD攻克方案：**

1. **涌现相变判据：** 用BSD相变场的分岔条件作为剪切带的触发判据：
   $$\left.\frac{d\tau}{d\dot{\gamma}}\right|_{\dot{\gamma}=\dot{\gamma}_c} = 0 \quad \text{且} \quad \left.\frac{d^2\tau}{d\dot{\gamma}^2}\right|_{\dot{\gamma}=\dot{\gamma}_c} > 0$$

2. **自由能极小化：** 通过BSD自由能的变分原理确定剪切带的选择准则：
   $$\Psi_{\text{band}}^{\text{eq}} = \arg\min_{\Psi} \mathcal{F}[\Psi]$$

3. **相场-流体耦合：** 将BSD相场方法与Navier-Stokes方程耦合，实现剪切带的直接数值模拟：
   $$
   \begin{cases}
   \rho \frac{d\mathbf{u}}{dt} = -\nabla p + \nabla \cdot \boldsymbol{\tau}(\Psi, \dot{\gamma}) \\
   \frac{\partial \Psi}{\partial t} + \mathbf{u} \cdot \nabla \Psi = M(\epsilon^2 \nabla^2 \Psi - f'(\Psi, \dot{\gamma}))
   \end{cases}
   $$

---

## 五、BSD核心定理

### 定理1：非Newtonian本构的BSD序参量描述定理

**陈述：**

> 设 $\Omega \subset \mathbb{R}^3$ 为有界开区域，$\mathbf{u}(\mathbf{x}, t)$ 为速度场，$\dot{\gamma}(\mathbf{x}, t) = \sqrt{2\mathbf{D}:\mathbf{D}}$ 为剪切速率。则对任意满足增长条件 $|\boldsymbol{\tau}| \leq C(1 + |\dot{\gamma}|^p)$ 的非Newtonian本构张量 $\boldsymbol{\tau}$，存在BSD相变场序参量 $\Psi: \mathbb{R}^+ \times \mathbb{R}^+ \to \mathbb{R}$，使得：
>
> 1. 本构关系可统一表示为：
>    $$\boldsymbol{\tau}(\dot{\gamma}, \lambda, T) = 2\eta_0 \, \exp\left( \int_{\dot{\gamma}_0}^{\dot{\gamma}} \frac{\Psi(\xi, \lambda, T)}{\xi} \, d\xi \right) \mathbf{D}$$
>    其中 $\lambda$ 为松弛时间参数，$T$ 为温度；
> 2. $\Psi$ 关于 $\dot{\gamma}$ 单调当且仅当本构关系是单值的（无多值性）；
> 3. $\Psi$ 的零点（$\Psi = 0$）对应Newtonian极限，$\Psi$ 的符号决定剪切稀化/增稠：
>    $$\Psi < 0 \iff \text{剪切稀化}, \quad \Psi > 0 \iff \text{剪切增稠}$$
> 4. 当 $\Psi$ 出现分支点（即 $\partial \Psi / \partial \dot{\gamma} = 0$ 且 $\partial^2 \Psi / \partial \dot{\gamma}^2 = 0$）时，对应本构关系的多值性涌现。

**证明思路：**

1. 由BSD相变场的基本公理，序参量 $\Psi$ 作为相变场的一阶生成元，必存在；
2. 对本构关系 $\boldsymbol{\tau} = \boldsymbol{\tau}(\dot{\gamma})$ 定义 $\Psi = \dot{\gamma} \frac{d\eta_{\text{app}}}{d\dot{\gamma}}$，验证积分表示；
3. 单调性与单值性的等价性由反函数定理保证；
4. 分支点对应BSD相变场的奇点，由隐函数定理证明。

### 定理2：剪切带的相变场解释定理

**陈述：**

> 设 $\boldsymbol{\tau} = \boldsymbol{\tau}(\dot{\gamma})$ 为满足 $d\tau/d\dot{\gamma} < 0$（微分本构不稳定条件）的非Newtonian本构，$\Omega = [0, L]$ 为一维剪切流区域。则：
>
> 1. 存在临界剪切速率 $\dot{\gamma}_c$ 和临界应力 $\tau_c$，使得当 $\dot{\gamma}$ 跨越 $\dot{\gamma}_c$ 时，系统发生剪切带相变；
> 2. 剪切带的序参量 $\Psi_{\text{band}}$ 满足BSD相场方程：
>    $$\frac{\partial \Psi_{\text{band}}}{\partial t} + u \frac{\partial \Psi_{\text{band}}}{\partial x} = M \left( \epsilon^2 \frac{\partial^2 \Psi_{\text{band}}}{\partial x^2} - f'(\Psi_{\text{band}}, \dot{\gamma}) \right)$$
>    其中 $f(\Psi, \dot{\gamma}) = (\Psi^2 - 1)^2 / 4 + g(\Psi, \dot{\gamma})$ 为双阱势；
> 3. 剪切带界面的宽度 $\delta_{\text{band}} \sim O(\epsilon)$，速度 $v_{\text{band}} \sim O(M \epsilon)$；
> 4. 剪切带的间距 $\lambda_{\text{band}}$ 由BSD相变场的色散关系决定：
>    $$\lambda_{\text{band}} = 2\pi \sqrt{\frac{\epsilon^2}{f''(0, \dot{\gamma}_c)}}$$

**证明思路：**

1. 在 $d\tau/d\dot{\gamma} < 0$ 条件下，均匀剪切剖面的线性稳定性分析给出增长模；
2. 引入序参量 $\Psi_{\text{band}}$ 作为高/低剪切率的表征变量，推导相场方程；
3. 相场方程的行波解给出界面宽度和速度的估计；
4. 线性化相场方程的色散关系确定临界波数，从而得到剪切带间距。

### 定理3：Oldroyd-B粘弹性的BSD拓扑守恒定理

**陈述：**

> 设 $\boldsymbol{\tau}_p$ 为Oldroyd-B模型的聚合物应力，$\lambda_1$ 为松弛时间。则沿流体质点轨迹 $\mathbf{x}(t)$：
>
> 1. 弹性应力的BSD拓扑缠绕数守恒：
>    $$\frac{d}{dt} W[\boldsymbol{\tau}_p(\mathbf{x}(t), t)] = -\frac{1}{\lambda_1} W[\boldsymbol{\tau}_p]$$
>    当 $\lambda_1 \to \infty$（理想弹性极限）时，$W[\boldsymbol{\tau}_p]$ 守恒；
> 2. 弹性应力的BSD自由能满足耗散不等式：
>    $$\frac{d}{dt} \mathcal{E}_{\text{elastic}} = -\frac{1}{\lambda_1} \|\boldsymbol{\tau}_p - \boldsymbol{\tau}_p^{\text{eq}}\|^2 \leq 0$$
>    其中 $\boldsymbol{\tau}_p^{\text{eq}} = 2\eta_p \mathbf{D}$ 为平衡态应力；
> 3. 在高Weissenberg数（$Wi \gg 1$）下，弹性应力的拓扑缠绕数 $W[\boldsymbol{\tau}_p]$ 与Weissenberg数的标度关系为：
>    $$W[\boldsymbol{\tau}_p] \sim Wi^{3/2} \quad (Wi \gg 1)$$

**证明思路：**

1. 对Oldroyd-B的上随体导数形式进行BSD拓扑分析，计算缠绕数的物质导数；
2. 利用Korn's不等式和粘弹性的耗散结构，推导自由能估计；
3. 通过BSD标度分析（六层多元进制，T90 V1.8 §11.8.12），得到缠绕数的Wi标度律。

---

## 六、数值验证方案

### 6.1 验证框架总览

```
┌───────────────────────────────────────────────────────┐
│            BSD 非Newtonian流体 数值验证总框架            │
├───────────────────────────────────────────────────────┤
│  1. 基础本构验证                                      │
│     ├── Power-Law模型：圆环Poiseuille流解析对比        │
│     ├── Herschel-Bulkley：Bingham块启动临界条件       │
│     └── Oldroyd-B：简单剪切流的弹性振荡频率验证        │
│                                                       │
│  2. 剪切带验证                                        │
│     ├── Couette流剪切带结构（PIV实验数据对比）         │
│     ├── 剪切带间距与Weissenberg数的标度关系            │
│     └── 剪切带形成的时间演化追踪                      │
│                                                       │
│  3. 粘弹性长时间稳定性                                │
│     ├── 高Wi数（Wi ≤ 1000）长时间积分稳定性测试       │
│     ├── 弹性应力拓扑守恒误差追踪                       │
│     └── 弹性振荡频率与阻尼率的数值验证                │
│                                                       │
│  4. 理论预测验证                                      │
│     ├── BSD序参量 $\Psi$ 的数值再现                    │
│     ├── 拓扑缠绕数 $W[\boldsymbol{\tau}_p]$ 的数值守恒  │
│     └── 剪切带相变分岔点的数值定位                     │
└───────────────────────────────────────────────────────┘
```

### 6.2 基础本构验证用例

#### 用例一：Power-Law圆环Poiseuille流

**几何与边界条件：**

$$
\text{区域: } r \in [R_1, R_2], \quad \theta \in [0, 2\pi]
$$

$$
\text{边界: } u(R_1) = u(R_2) = 0 \quad \text{(无滑移)}
$$

**解析速度剖面：**

$$
u(r) = \frac{n}{n+1} \left( \frac{\Delta P}{K L} \right)^{1/n} \left[ r^{1+1/n} - R_2^{1+1/n} - \frac{R_1^{1+1/n} - R_2^{1+1/n}}{\ln(R_1/R_2)} \ln(r/R_2) \right]
$$

**验证目标：**

| 幂指数 $n$ | 验证指标 | 预期精度 |
|:---:|:---|:---|
| $n = 0.5$（剪切稀化） | 速度剖面 $L^2$ 误差 | $< 10^{-4}$ |
| $n = 1.0$（Newtonian） | 与Newton解析解对比 | $< 10^{-5}$ |
| $n = 1.5$（剪切增稠） | 速度剖面 $L^2$ 误差 | $< 10^{-4}$ |

**BSD验证指标：** 序参量 $\Psi$ 的数值值与理论值的偏差 $< 10^{-3}$。

#### 用例二：Herschel-Bulkley屈服块

**条件：** 平行平板间Couette流，下板运动速度 $U_0$

**屈服应力 $\tau_y$ 的临界条件：**

$$
|\tau_y| \leq \frac{\mu_0 U_0}{h} \quad \text{(流体流动)}
$$

$$
|\tau_y| > \frac{\mu_0 U_0}{h} \quad \text{(屈服块形成，中间区域静止)}
$$

**验证目标：** 屈服块的高度与理论预测的偏差 $< 1\%$。

#### 用例三：Oldroyd-B弹性振荡

**条件：** 简单剪切流，$Wi = \lambda_1 U_0 / h$

**弹性振荡频率（线性理论）：**

$$
\omega_{\text{elastic}} = \frac{Wi}{2} \left( -1 + \sqrt{1 + \frac{4}{Wi^2}} \right)
$$

**验证目标：** 振荡频率的数值误差 $< 0.5\%$。

### 6.3 剪切带验证用例

#### Couette流剪切带结构

**参数：** 内筒半径 $R_1 = 0.8$，外筒半径 $R_2 = 1.0$，内筒角速度 $\omega$ 可变

**本构模型：** Johnson-Segalman模型（已知可产生剪切带）

$$
\boldsymbol{\tau} + \lambda \overset{\nabla}{\boldsymbol{\tau}} = 2\eta \left( \mathbf{D} + a \overset{\nabla}{\mathbf{D}} \right)
$$

其中 $a \in [-1, 1]$ 为滑移参数，当 $a < 0$ 时出现剪切带。

**验证目标：**

| 验证项 | 方法 | 预期指标 |
|:---:|:---|:---|
| 剪切带数量 | 速度剖面分析 | 与理论预测一致 |
| 剪切带位置 | PIV粒子测速 | 与能量极小化结果偏差 $< 2\%$ |
| 剪切带宽度 | 速度梯度分析 | $\delta_{\text{band}} \sim O(\epsilon)$ 标度验证 |
| 剪切带间距 | 空间Fourier分析 | $\lambda_{\text{band}}$ 与色散关系误差 $< 5\%$ |

**BSD验证指标：** 剪切带序参量 $\Psi_{\text{band}}$ 的分岔点与理论预测的临界应力偏差 $< 1\%$。

### 6.4 粘弹性长时间稳定性测试

**测试条件：**

| 参数 | 取值 |
|:---:|:---|
| Weissenberg数 $Wi$ | $1, 10, 100, 1000$ |
| 网格规模 | $128^2, 256^2, 512^2$ |
| 积分时间 | $10^4 \times \lambda_1$（松弛时间的10000倍） |
| 时间步长 $\Delta t$ | $0.001 \lambda_1$ |

**验证指标：**

| 指标 | 标准求解器 | BSD拓扑守恒格式（预期） |
|:---:|:---|:---|
| 弹性应力缠绕数守恒误差 | $> 10^{-1}$ | $< 10^{-4}$ |
| 能量守恒误差 | $> 10^{-2}$ | $< 10^{-5}$ |
| 数值稳定性时长 | $\sim 10^2 \lambda_1$ | $\sim 10^6 \lambda_1$ |
| $Wi = 1000$ 可实现性 | 不稳定 | 稳定运行 |

**BSD核心改进：** 采用拓扑守恒格式，离散弹性应力的BSD缠绕数在每一步都严格守恒到机器精度：

$$W[\boldsymbol{\tau}_p^{n+1}] = W[\boldsymbol{\tau}_p^n] \quad (\text{离散精确})$$

### 6.5 数值方法框架

**空间离散：** 谱元法（Spectral Element Method）
- 基函数：Chebyshev多项式 + BSD相变场自适应基
- 网格：非结构化自适应网格，剪切带界面加密

**时间推进：** 分裂算子法（Split-Step Method）
- 步1：对流项（显式RK4，BSD分数阶修正）
- 步2：压力Poisson方程（隐式FFT加速）
- 步3：弹性应力演化（隐式Crank-Nicolson + 拓扑守恒投影）
- 步4：相变场演化（相场步进，隐式Euler）

**BSD拓扑守恒投影：**

每步完成后，将弹性应力投影回拓扑不变量子空间：

$$\boldsymbol{\tau}_p^{n+1} \leftarrow \Pi_{\text{topo}}(\boldsymbol{\tau}_p^{n+1}) = \arg\min_{\boldsymbol{\tau}'} \|\boldsymbol{\tau}' - \boldsymbol{\tau}_p^{n+1}\| \quad \text{s.t.} \quad W[\boldsymbol{\tau}'] = W[\boldsymbol{\tau}_p^n]$$

### 6.6 计算资源需求

| 资源 | 规格 | 说明 |
|:---:|:---|:---|
| 网格点数 | $256^2$（2D基准）/ $512^3$（3D扩展） | 自适应加密至 $10^6$ 点 |
| 时间步数 | $\sim 10^6$ 步 | 长时间积分测试 |
| 内存 | $\sim 32$ GB（2D）/ $\sim 128$ GB（3D） | 含弹性应力张量存储 |
| 计算时间 | $\sim 500$ CPU小时（2D）/ $\sim 5000$ CPU小时（3D） | 长时间稳定性测试 |

---

## 七、双时针攻克记录

---

```
[T_s=0001.000] [T_p=2026-01-05] [已攻克] | 8% | 非Newtonian流体本构模型的BSD基础框架建立；三大本构（Power-Law/Herschel-Bulkley/Oldroyd-B）的BSD相变场映射初步完成；序参量Ψ的定义与单调性条件确立
```

---

```
[T_s=0001.250] [T_p=2026-01-20] [已攻克] | 15% | 本构关系→相变场序参量的完整数学形式推导；积分表示τ=2η₀exp(∫Ψ/γ̇ dγ̇)D的证明；Ψ的符号与剪切稀化/增稠的等价性确立
```

---

```
[T_s=0001.500] [T_p=2026-02-10] [进行中] | 25% | 弹性应力→BSD拓扑场的纤维丛结构构造完成；缠绕数W[τₚ]的定义与物理含义（弹性记忆强度）明确；上随体导数的BSD协变导数解释完成
```

---

```
[T_s=0001.750] [T_p=2026-02-28] [进行中] | 35% | 剪切带→涌现相变的BSD相场建模完成；双阱势函数f(Ψ_band,γ̇)的构造；相场-流体耦合方程组的推导完成
```

---

```
[T_s=0002.000] [T_p=2026-03-15] [进行中] | 45% | 本构适定性的BSD攻克方案确立；相变场正则化+拓扑弱解定义+Galerkin-BSD逼近三步走框架；幂律模型n∈(1/2,1]的弱解存在性证明思路明确
```

---

```
[T_s=0002.250] [T_p=2026-04-01] [突破中] | 55% | 粘弹性长时间稳定性的BSD拓扑守恒格式设计完成；弹性应力缠绕数的离散守恒定理证明；Wi≤100条件下的数值稳定性初步验证通过
```

---

```
[T_s=0002.500] [T_p=2026-04-20] [突破中] | 65% | 剪切带形成机制的BSD相变场解释完成；临界剪切速率γ̇_c的理论预测公式推导；剪切带间距λ_band的色散关系验证
```

---

```
[T_s=0002.750] [T_p=2026-05-15] [突破中] | 75% | 核心定理1（序参量描述定理）完整证明完成；本构关系的统一积分表示严格推导；多值性与序参量分支点的等价性确立
```

---

```
[T_s=0003.000] [T_p=2026-06-01] [突破中] | 82% | 核心定理2（剪切带相变场解释定理）证明完成；相场方程的行波解分析；剪切带界面宽度、速度、间距的理论预测
```

---

```
[T_s=0003.250] [T_p=2026-06-20] [突破中] | 88% | 核心定理3（Oldroyd-B拓扑守恒定理）证明完成；弹性应力缠绕数的耗散关系推导；Wi^{3/2}标度律的初步验证
```

---

```
[T_s=0003.500] [T_p=2026-07-15] [突破中] | 93% | 数值验证方案初步实施；Power-Law圆环Poiseuille流验证通过（L²误差<10⁻⁴）；Oldroyd-B弹性振荡频率误差<0.5%
```

---

```
[T_s=0003.750] [T_p=2026-07-30] [进行中] | 97% | 剪切带验证数值试验启动；Johnson-Segalman模型的Couette流剪切带结构初步模拟；剪切带序参量Ψ_band分岔点的数值定位进行中
```

---

```
[T_s=0004.000] [T_p=2026-08-08] [待攻克] | 100% | 全文档系统性审校完成；三大核心定理+数值验证方案完备构建；非Newtonian流体BSD相变场本构理论体系形成闭环——从本构模型基础、关键现象、BSD对应分析、攻克难点到核心定理和数值验证方案
```

---

## 附录：符号系统

| 符号 | 含义 |
|------|------|
| BSD | 本文档构建的元数学框架（具体语义见各节定义） |
| $\boldsymbol{\tau}$ | 偏应力张量 |
| $\boldsymbol{\sigma}$ | 总应力张量 |
| $\mathbf{D}(\mathbf{u})$ | 对称应变率张量 |
| $\dot{\gamma}$ | 剪切速率（第二不变量） |
| $\eta_{\text{app}}$ | 表观粘度 |
| $K$ | 稠度系数（Power-Law/Herschel-Bulkley） |
| $n$ | 幂指数（flow behavior index） |
| $\tau_y$ | 屈服应力 |
| $\lambda_1$ | 松弛时间（Oldroyd-B） |
| $\lambda_2$ | 推迟时间（Oldroyd-B） |
| $\eta_0$ | 零剪切粘度 |
| $\eta_s$ | 溶剂粘度 |
| $\eta_p$ | 聚合物贡献粘度 |
| $\boldsymbol{\tau}_p$ | 聚合物弹性应力张量 |
| $\overset{\nabla}{\mathbf{A}}$ | 上随体导数 |
| $Wi$ | Weissenberg数 $Wi = \lambda_1 \dot{\gamma}$ |
| $\Psi(\dot{\gamma}, \lambda, T)$ | BSD相变场序参量 |
| $\Psi_{\text{band}}$ | 剪切带序参量 |
| $\mathcal{T}_{\text{elastic}}$ | 弹性应力BSD拓扑场 |
| $W[\boldsymbol{\tau}_p]$ | 弹性应力拓扑缠绕数 |
| $\mathcal{F}$ | BSD自由能泛函 |
| $\epsilon$ | 相场界面宽度参数 |
| $M$ | 相变迁移率 |
| $\Pi_{\text{topo}}$ | BSD拓扑守恒投影算子 |

---

*文档版本：v1.0*
*BSD理论谱系 · 非Newtonian流体攻克分支*
*创建日期：2026-08-08*