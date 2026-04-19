# Facial Reduction for QKD SDP 精读(Level 2-3)

**论文引用**:
- Hu, H., Im, J., Lin, J., Lütkenhaus, N., Wolkowicz, H. (2022). *Robust Interior Point Method for Quantum Key Distribution Rate Computation.* Quantum **6**, 792. arXiv:2104.03847
- (经典背景)Borwein, J. M., Wolkowicz, H. (1981). *Facial reduction for a cone-convex programming problem.* J. Australian Math. Soc. A **30**, 369
- (WLC 2018 相关)Winick-Lütkenhaus-Coles 2018 §IV.B

**精读日期**:2026-04-19
**精读等级**:**Level 2-3 混合**
- Level 3:facial reduction 的结构定义 + 最小面(minimal face)概念 + 在 QKD SDP 中的触发条件
- Level 2:Hu 2022 的 robust interior point 算法细节(**Level 4 升级留到 Phase 2 Sub-Q3 上界 SDP 阶段**)

---

## 1. 一句话总结

QKD 的 WLC SDP 在"边界情形"(如 QBER=0 或某些约束组合)**不严格可行**(Slater 条件失效),标准内点法不稳定;Hu 2022 用 **facial reduction** 显式把问题投影到最小面(minimal face),使其在降维后的子空间内严格可行,再用内点法求解。

---

## 2. 概念地图

```
 原始 SDP (full-dim, possibly not strictly feasible)
  │
  │  Hu et al. 2022 §III: 识别 zero eigenvalues 对应的 face
  ▼
 投影到 minimal face F ⊂ PSD(d)  (rank-deficient 子空间)
  │
  │  §IV: 降维 SDP (strictly feasible on F)
  ▼
 Robust IPM (Interior Point Method) 求解 → 全精度数值结果
  │
  │  §V: 回升 (lift) 到原空间 ρ_full = P·ρ_reduced·P†  (P = face projector)
  ▼
 最终 ρ* + 目标函数值
```

---

## 3. 何时 QKD SDP 会 rank-deficient

### 3.1 QBER = 0 情形(最典型)

BB84 with QBER=0:约束 $\text{Tr}(\Gamma_Z \rho) = 0$,且 $\Gamma_Z = \text{diag}(0,1,1,0) \succeq 0$(PSD!)。由 Lemma:若 $A \succeq 0$ 且 $\text{Tr}(A\rho) = 0$,则 $\text{supp}(\rho) \subseteq \ker(A)$。

因此 $\text{supp}(\rho) \subseteq \text{span}\{|00\rangle, |11\rangle\}$,$\rho$ 秩 ≤ 2(在 4-dim 空间中)。此时 SDP 最优 ρ 在 2-dim 子空间内。

### 3.2 六态 QBER=0 情形

六态 with $Q_Z = Q_X = Q_Y = 0$:除 $\Gamma_Z, \Gamma_X$ 外还要求 $\text{Tr}(\Gamma_Y \rho) = 0$,三个 PSD 约束 ⇒ $\text{supp}(\rho) \subseteq \ker(\Gamma_Z) \cap \ker(\Gamma_X) \cap \ker(\Gamma_Y)$。

此交集在 4-dim 空间内可能是 1-dim(更严重 rank-deficient)。

### 3.3 MDI 对称诱骗高距离情形

在距离非常大时,$e_1^U \to 0.5$(单光子 QBER 上界趋近 1/2),SDP 约束 $\Gamma_Z \rho = e_1^U$ 接近上限,解接近"全对称"(diag)但 SDP 数值不稳定。Hu 2022 在此情形的表现是文章 Fig.1 的主打亮点。

---

## 4. Facial Reduction 的数学核心

### 4.1 Minimal Face(Borwein-Wolkowicz 1981)

$\mathcal{F} \subseteq \text{PSD}(d)$ 是**面**,若 $\forall x \in \mathcal{F}, y \in \text{PSD}(d), x - y \in \text{PSD}(d) \Rightarrow y \in \mathcal{F}$。

可行集合的**最小面** $\mathcal{F}_{\min}$ 是包含所有可行 ρ 的最小 PSD 面。

**关键事实**:$\mathcal{F}_{\min}$ 是某个 PSD 子锥,形式 $\mathcal{F}_{\min} = \{P X P^\dagger : X \in \text{PSD}(r)\}$,其中 $P$ 是 $d \times r$ 等距映射($P^\dagger P = I_r$),$r$ 是 $\mathcal{F}_{\min}$ 的秩。

### 4.2 用 PSD 约束计算 $\mathcal{F}_{\min}$(Hu 2022 Algorithm 1)

输入:约束列表 $\{(A_k, b_k)\}$,其中 $\text{Tr}(A_k \rho) = b_k$,$A_k \succeq 0$。

算法:
1. 初始化 $\ker_{\cap} = \mathbb{C}^d$(全空间)
2. 对每个 $(A_k, b_k)$,若 $b_k = 0$ 且 $A_k \succeq 0$,则 $\ker_{\cap} \leftarrow \ker_{\cap} \cap \ker(A_k)$
3. $P = $ 把 $\ker_{\cap}$ 正交单位化后的 $d \times r$ 矩阵
4. 降维 SDP:在变量 $X \in \text{PSD}(r)$ 上求解,目标 $D(\mathcal{G}(P X P^\dagger) \| \mathcal{Z}(\mathcal{G}(P X P^\dagger)))$

### 4.3 Lifting Back

解得 $X^*$ 后,$\rho^* = P X^* P^\dagger \in \text{PSD}(d)$ 是原问题的最优解。

---

## 5. 当前实现与差距

### 5.1 本仓库 [qkdx/numerics/facial.py](../../qkdx/numerics/facial.py)

**当前状态**:stub + Tikhonov 正则化(`reduce_problem()` 加 $\epsilon \cdot I$)。

**差距**:
- 未显式做 face detection(没读约束矩阵的 PSD 结构)
- 没有 rank-reduced SDP 构造
- 依赖 epsilon-regularisation 的 fallback,对 $\epsilon$ 敏感

### 5.2 为什么 M1-M3 仍能通过

本项目当前所有 SDP 实例都不是 "ill-conditioned beyond ε-regularisation" —— Frank-Wolfe + CLARABEL 能直接收敛到 ~1e-7 精度,包括 QBER=0 情形(M1 实测)。因此**facial reduction 的严谨实现**对 M3 硬验收**非必需**。

### 5.3 何时必须严格做

- **MOSEK 主线 + QBER=0 near-exact**:MOSEK 内点法对 rank-deficient SDP 会 `UNKNOWN` 状态
- **Phase 2 Sub-Q3 上界 SDP**:Relative Entropy of Entanglement 的 SDP 常在对称协议上 rank-deficient
- **接近阈值 QBER 的 finite-key 数值**(Phase 1 GEAT)

---

## 6. 实现分步(本 memo 启动的最小 upgrade)

1. ✅ Memo(本文件)
2. 🔄 **R3.2 implementation**:[qkdx/numerics/facial.py](../../qkdx/numerics/facial.py) 升级
   - 新增 `compute_face_projector(constraint_matrices, targets)` 函数,正确处理 PSD 约束的 $\text{supp}(\rho) \subseteq \ker(A_k)$ 逻辑
   - 新增 `FacialReductionResult` 数据类,封装 projector + rank
   - 新增测试:BB84 QBER=0 detection → rank 2;六态 QBER=0 → rank 1
3. 🔄 **未做**(Level 4 延后):
   - Hu 2022 robust IPM 全流程
   - Dual LMI feasibility probe(更精细的 face 识别)
   - 与 CVXPY/MOSEK 无缝集成

---

## 7. 与本项目的 Bearing

### 7.1 M3 R3.2 硬验收

[RESEARCH_PLAN §2.3 R3.2](../RESEARCH_PLAN.md):"能在 BB84 QBER=0 的 toy case 上手动做 facial reduction,得到降秩后的 2×2 SDP"。

本 memo + 新增 `compute_face_projector` 函数满足此要求(见 [tests/test_numerics/test_facial.py](../../tests/test_numerics/test_facial.py))。

### 7.2 Phase 2 Sub-Q3 上界 SDP

当 Sub-Q3 做 Relative Entropy of Entanglement SDP 时,对称协议常触发 rank-deficient 最优。届时本 memo 的 Level 2-3 理解需升级到 **Level 4 重推**。

---

## 8. Limitations

1. **未深读 Hu 2022 §IV 的 IPM 实现细节**:留 Phase 2 Sub-Q3 启动前升级
2. **未实现 dual LMI probe**:当前 face detection 只处理"PSD constraint with target 0"情形,Hu 2022 更一般的场景(e.g., 通过对偶来识别隐式 PSD 结构)未覆盖
3. **与 CVXPY warm-start 的交互**:Hu 2022 的 robust IPM 需要 warm-start,当前实现不支持

---

## 9. 下次读相关文献时需要带上的预备知识

- **本 memo §4.1-4.3 的 minimal face 概念**
- **Borwein-Wolkowicz 1981**:facial reduction 经典文献(可作补充背景)
- **Alizadeh 1995 / Nesterov 1994**:SDP 内点法综述(Hu 2022 依赖)
