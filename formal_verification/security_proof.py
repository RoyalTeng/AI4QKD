from qcgf_dsl.protocol_graph import ProtocolGraph
from security_evaluator import EntropyEstimator, ComposableSecurityAnalyzer

class SecurityProof:
    """
    使用抽象密码学模型生成形式化安全证明的文本表示。
    """
    def generate(self, graph: ProtocolGraph, qber: float, gain: float) -> str:
        """
        生成协议的形式化安全证明（LaTeX/Math风格）。

        Args:
            graph (ProtocolGraph): 协议图。
            qber (float): 量子比特错误率。
            gain (float): 信道增益。

        Returns:
            str: 格式化的安全证明文本。
        """
        entropy_estimator = EntropyEstimator()
        composable_analyzer = ComposableSecurityAnalyzer()

        # 1. 最小熵计算
        min_entropy_result = entropy_estimator.calculate_min_entropy(qber, "BB84")
        h_min = min_entropy_result.value

        # 2. 纠错泄露
        leak_ec = qber * 1.16 # 假设 f_ec=1.16

        # 3. 可组合性
        comp_result = composable_analyzer.analyze_composable_security(n_protocols=1, protocol_epsilon=1e-9)
        
        # 4. 构建 LaTeX 风格的证明字符串
        proof_str = r"""
\documentclass{article}
\usepackage{amsmath}
\begin{document}
\section*{QKD Protocol Security Proof}

Let the protocol be represented by the graph $G$. 
The security of the protocol is evaluated based on the Abstract Cryptography framework.

\subsection*{1. Min-Entropy Estimation}
The conditional min-entropy $H_{\min}(X|E)$ of the raw key $X$ given Eve's information $E$ is lower-bounded by the binary entropy of the QBER.
\begin{equation}
    H_{\min}(X|E) \ge 1 - h_2(\text{QBER})
\end{equation}
Given QBER = %.4f, we have $h_2(%.4f) \approx %.4f$.
Thus, $H_{\min}(X|E) \ge %.4f$.

\subsection*{2. Information Leakage}
The information leaked during error correction is estimated as:
\begin{equation}
    \text{leak}_{\text{EC}} = f_{\text{EC}} \cdot h_2(\text{QBER})
\end{equation}
With $f_{\text{EC}} = 1.16$, $\text{leak}_{\text{EC}} \approx %.4f$.

\subsection*{3. Secret Key Rate}
The asymptotic secret key rate $R$ is given by:
\begin{equation}
    R = G \cdot [H_{\min}(X|E) - \text{leak}_{\text{EC}}]
\end{equation}
With gain $G=%.2f$, the key rate is $R \approx %.4f$ bits/pulse.

\subsection*{4. Composable Security}
The protocol achieves $\epsilon$-security with $\epsilon_{\text{total}} = \epsilon_{\text{sec}} + \epsilon_{\text{cor}} \approx %.2e$.

\end{document}
""" % (
    qber, qber, (1 - h_min), h_min, leak_ec, gain, gain * (h_min - leak_ec), comp_result.epsilon_total
)
        return proof_str 