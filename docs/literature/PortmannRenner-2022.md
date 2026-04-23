# Portmann-Renner 2022 — **[PDF-NEEDED, STUB ONLY]**

**Reference**: Portmann, C., Renner, R. (2022). *Security in quantum cryptography*. Rev. Mod. Phys. **94**:025008.

**Status** (2026-04-23): **PDF not in `docs/literature/pdfs/`**. 本 memo 是 **stub ONLY** — 记录 project relevance + 需读章节, **不**含实际 Level 2/3 精读内容.

---

## 0. Why this paper matters for AI4QKD

### 0.1 β.G4 Eve model transfer potential closure path

Per [umr_path_beta_G4_derivation_attempt.md](../proofs/umr_path_beta_G4_derivation_attempt.md) §3.1 **Path C**:

> "Portmann-Renner composable framework **explicitly** handle umr adversary class without reduction to LOPC"

β.G4 的 direct simulation map approach (§2.3-§2.5) 已证 **fails** — 没有 trivial 办法 show umr Eve class $\subseteq$ LOPC Eve class. Path C 假设 P-R 2022 framework 可以 direct handle umr (即 composable security for arbitrary adversary class 不需 LOPC reduction). **需 PDF verify**.

### 0.2 γ.G3 ε-composable transfer

Per [umr_path_gamma_v0_6_detailed_draft.md](../proofs/umr_path_gamma_v0_6_detailed_draft.md) §5, γ.G3 gap 是 "asymptotic $E_R$ bound → ε-composable finite-$n$ rate bound". P-R 2022 是 composable security 的 canonical reference.

### 0.3 R0.2 C1 pathway

R0.2 C1 需 "independent validation" not AI-only. P-R 2022 是 human-authored 严谨 framework — 若 user 直读 PDF + 基于 framework 构造 umr-specific proof, 这 qualify as C1(b) path.

---

## 1. 需要读的章节（based on AI memory [RECALLED])

估计以下章节对本 project 最相关 (未 PDF 核对, 用户请自行 verify TOC):

| 章节 | 估计内容 | 对应 AI4QKD 用途 |
|---|---|---|
| §II | Framework for composable security | β.G4 Path C, γ.G3 |
| §III | Distance measures (trace distance, fidelity, etc.) | γ.B.G1 quantum DPI foundations |
| §IV | Security of key distribution | umr security definition |
| §V | Information-theoretic constructions | Portmann-Renner primitives |
| §VI-VII | Composable vs non-composable security | Bridge to Khatri-Wilde Ch 20 |

**以上是 AI 推测, 非 PDF-verified TOC**.

---

## 2. 如何获取 PDF

### 2.1 Online source (user action)

- Rev. Mod. Phys. 94:025008 (2022) — APS membership 或 institutional access
- arXiv preprint 可能存在 — search arXiv 作者 Portmann + Renner 2022

### 2.2 建议存放位置

`docs/literature/pdfs/PortmannRenner-2022-SecurityQuantumCryptography.pdf` (参考其他 memo 文件名约定)

### 2.3 PDF 添加后

- 升级本 memo 从 **stub** 到 Level 2 (~50-80 页浏览, 10-15 页精读)
- 或 Level 3 (每个 theorem 对照 PDF 原文 + relevance analysis)
- 特别注意: framework 是否 handle untrusted relay / adversarial helper 的 composable security

---

## 3. AI autonomous 不做的事

- 不基于 [RECALLED] 记忆推导 Portmann-Renner theorems
- 不声明 P-R 2022 "handles umr" 前 PDF verify
- 不 upgrade β.G4 或 γ.G3 基于 [RECALLED] P-R

---

## 4. 目前状态对 user

用户需 action:
1. Obtain Portmann-Renner 2022 PDF (APS 或 arXiv)
2. Put at `docs/literature/pdfs/PortmannRenner-2022-SecurityQuantumCryptography.pdf`
3. 后续 AI session 可基于 PDF 做 Level 2/3 精读 → 实际 Level 2/3 memo
4. 或 user 自己 Level 3 精读 → user research-level proof on β.G4 / γ.G3

---

## Changelog

- **v0.1 STUB** (2026-04-23, AI autonomous session): Stub created because PDF not locally available. Project relevance recorded. PDF acquisition action for user.
