The provided paper, *"The Probability of Backtest Overfitting"* by Bailey et al. (2014), does not describe a specific trading strategy (like a moving average crossover). Instead, it provides a **meta-strategy logic** for evaluating and selecting investment strategies while controlling for the risk of **backtest overfitting**.

The core logic is centered on a method called **Combinatorially Symmetric Cross-Validation (CSCV)**. Here is the extraction of the strategy selection and evaluation logic:

---

### 1. The Core Objective
The logic aims to determine if the "optimal" strategy found during a backtest is likely to perform well in the future, or if its performance is merely a result of "cherry-picking" from a large number of trials ($N$).

### 2. The CSCV Procedure (Step-by-Step Logic)
The paper outlines a non-parametric numerical method to estimate the **Probability of Backtest Overfitting (PBO)**:

1.  **Matrix Construction ($M$):** Collect the performance time series (returns) of $N$ different strategy configurations into a matrix of order $T \times N$. 
    *   $T$ = Number of observations (rows).
    *   $N$ = Number of strategy trials (columns).
2.  **Partitioning:** Divide the $T$ observations into an even number of disjoint submatrices $S$ (e.g., $S=16$).
3.  **Combinatorial Pairing:** Form all possible combinations of these submatrices by taking groups of size $S/2$. 
    *   For each combination, one set of $S/2$ blocks forms the **In-Sample (IS)** set.
    *   the remaining $S/2$ blocks form the **Out-of-Sample (OOS)** set.
4.  **Optimization (IS):** For each combination, identify the strategy (column $n^*$) that achieves the best performance (e.g., highest Sharpe Ratio) in the IS set.
5.  **Evaluation (OOS):** Measure the performance and the **relative rank** ($\bar{\omega}$) of that same strategy ($n^*$) in the OOS set.
6.  **Logit Transformation:** Convert the relative rank into a logit value $\lambda = \ln(\bar{\omega} / (1-\bar{\omega}))$.
7.  **Distribution Analysis:** Collect logits from all combinations to form a distribution $f(\lambda)$.

### 3. Key Strategy Evaluation Metrics
The logic extracts four specific statistics to decide if a strategy should be deployed:

*   **PBO (Probability of Backtest Overfitting):** The probability that the IS-optimal strategy will underperform the median of all $N$ trials OOS.
    *   If **PBO > 0.5**, the selection process is detrimental (you would be better off picking a strategy at random).
*   **Performance Degradation:** A regression of IS performance vs. OOS performance. 
    *   **Logic:** A steep negative slope indicates that "the more you optimize IS, the worse you perform OOS." This is a hallmark of overfitting.
*   **Probability of Loss:** The frequency with which the IS-optimal strategy produces a negative return (or Sharpe Ratio) in the OOS sets.
*   **Stochastic Dominance:** A test to see if the IS-selection process consistently outperforms a random selection across different utility functions.

### 4. Overfitting Logic (The "Paradox")
The paper identifies a specific logical trap in strategy selection:
*   **Selection Bias:** As the number of trials ($N$) increases, the expected maximum Sharpe Ratio IS increases even if the true expected return of all strategies is zero.
*   **The Threshold:** Overfitting is not a "true or false" state but a probability. The paper argues that standard "hold-out" (test set) methods are insufficient because they don't account for the number of trials $N$ attempted before the final result was chosen.

### 5. Application Summary
To use this logic to select a strategy:
1.  **Don't just look at the best backtest.**
2.  Run the CSCV algorithm on **all** trials attempted during the research phase.
3.  Calculate the **PBO**.
4.  **Decision Rule:** Reject the "optimal" strategy if the PBO is high (typically > 0.10 or 0.20 depending on risk appetite), or if the OOS performance shows significant degradation compared to IS performance.

### 6. Mathematical Definition of Overfitting
The paper formally defines a backtest selection process as overfit if:
$$\sum_{n=1}^{N} E[r_n | r \in \Omega_n^*] \text{Prob}[r \in \Omega_n^*] \le N/2$$
*In plain English:* The process is overfit if the strategy you picked as "the best" IS has an expected rank that is worse than the median rank OOS.