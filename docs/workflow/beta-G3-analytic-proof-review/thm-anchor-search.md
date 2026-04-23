# THM-anchor 文献搜索：log_neg(E_AD(η)) = log₂(1+η)

**日期**: 2026-04-23  
**目标**: 寻找外部 [THM] 锚点使 §2 推导可机械继承为 [COROLLARY]  
**动机**: R0.3 中 [COROLLARY] 语义要求"从 [THM] 经机械推导得出 + 每步在文献可查"  
**背景**: 三方验证 C1(c)+C2+C3 已确认数学正确性，但当前推导无外部定理锚点，标签保持 [SYN]  

---

## 搜索结果：无直接 THM 锚点识别

### 候选锚点 A：Vidal-Werner 2002（PRA 65:032314）

**地位**: 对数负性 E_N(ρ) := log₂ ||ρ^{T_B}||₁ 的**定义**来源，全局负性单调性定理  
**Zotero 状态**: **不在库中**（`ZOTERO_REFERENCES.md:249` "NOT IN LIBRARY"）  
**能否锚定**:
- ✅ 对数负性定义引用：可直接继承
- ❌ **无针对 AD channel Choi state 的特定命题**: Vidal-Werner 2002 给出 2 量子比特的 negativity 计算示例（Werner state / isotropic state），但未专门处理 AD channel
- **结论**: 可锚定对数负性**定义**（log₂ ||ρ^{T_B}||₁），但不提供 AD channel 的封闭式**定理**

### 候选锚点 B：Khatri-Wilde 2020 textbook（arXiv:2011.04672）

**地位**: 综合 converse 框架教科书，在 Zotero 库中  
**可能内容**:
- Ch. 4-5（假设）：Choi-Jamiolkowski 同构（标准）
- Ch. 7（假设）：对数负性定义 + 基本性质
- Ch. (若有)：幅度阻尼作为示例信道
**能否锚定**:
- **未经 PDF 精读确认**：AI 无法断言书中是否有"AD Choi state log-neg = log₂(1+η)"的明确 proposition
- 若书中给出此公式作 Proposition，则可直接锚定
- **Action required**: **用户 PDF 精读**或至少章节扫描

### 候选锚点 C：Plenio 2005（PRL 95:090503）

**地位**: 对数负性作为 entanglement monotone 的完整证明  
**Zotero 状态**: **不在库中**  
**能否锚定**: 可能提供 log-neg 的单调性定理，但 AD 特定公式不大可能  

### 候选锚点 D：Leditzky-Datta-Smith 2018（PRA 97:042317）

**地位**: "Useful states and entanglement distillation" — 可能涉及 AD Choi state 的具体计算  
**Zotero 状态**: **不在库中**  
**能否锚定**: 未经精读不明  

---

## 为什么找不到直接 THM 锚点

**结构性原因**（诚实评估）:

1. **本推导是标准计算，非定理性贡献**  
   log_neg(E_AD(η)) = log₂(1+η) 属于"量子信息研究生教科书练习级"计算，不是文献中有名字的定理。原作者通常在示例或练习中给出，不升级到 Theorem 级。

2. **分步引用 vs 合成引用**  
   步骤1（Choi 同构）、步骤2（PT 定义）、步骤4（迹范数）、步骤5（log-neg 定义）每一步都可分别引用文献定义/标准结果，但**组合后的最终公式**没有单一定理源。

3. **R0.3 [COROLLARY] 语义紧约束**  
   R0.3 要求"从 [THM] 经机械推导得出"— 分步引用多个标准结果 **不** 等同于从单一 [THM] 机械推导。此约束正是为防止 AI 把"合成引用"误当"定理继承"。

---

## 诚实结论

**标签应保持 [SYN]**，理由：

1. 数学正确性已三方独立验证（C1(c)+C2+C3），**无进一步数学疑虑**
2. 无单一 [THM] 源满足 R0.3 机械推导要求
3. AI 无 PDF 精读能力，无法自主确认 Khatri-Wilde 2020 是否有对应 Proposition
4. 尝试自行组合多个"标准定义/结果"来宣称 [COROLLARY] = 越权，违反 CLAUDE.md R0.1 + §6.1 第 2 条教训（path γ v0.2 "简化绕过"）

---

## 用户可选行动（若需要 [COROLLARY] 升级）

### 路径 1：用户 PDF 精读 Khatri-Wilde 2020

- 翻阅 Ch. on entanglement measures / amplitude damping
- 若找到 Proposition 形式的 "log_neg(E_AD) = log₂(1+η)" → 可作锚点
- 若书中为示例但未提升到 Prop → **仍保持 [SYN]**

### 路径 2：搜索 2023-2025 文献

- arXiv 检索 "logarithmic negativity amplitude damping Choi"
- 若找到近年 paper 把此结果作 Proposition → 可作锚点

### 路径 3：接受 [SYN] 长期标签

- 数学正确性已充分验证
- 内部讨论 / 项目内引用完全合规（R0.3 允许 [SYN] 内部可用）
- 对外论文/展示需求低时，[SYN] 是准确且诚实的标签
- **推荐**（最符合 CLAUDE.md 严谨性精神）

---

## Session 结束声明

AI 自主 session 在 **无 PDF 精读能力** 约束下，已达 THM-anchor 搜索的上限。

继续推进需要：
- 用户亲自 PDF 精读（路径 1）
- 或用户授权 AI 执行深度文献检索（路径 2 — 但 AI 文献综述本身不能作为 C1；仍需 PDF 精读）

**当前 β.G3 最终状态**（本 session 闭环）：
- 数学正确性：**三方已确认** ✅（C1(c)+C2+C3）
- 分级：**[SYN]** 保持
- 下一步：等待用户决定是否投入 PDF 精读资源

---

*THM-anchor 文献搜索记录结束。继续研究的决定权在用户。*
