Based on the paper **"Dealing with the Inventory Risk: A solution to the market making problem"** by Guéant, Lehalle, and Fernandez-Tapia, the strategy logic can be extracted as follows:

### 1. Objective and Framework
The strategy is designed for a **High-Frequency Market Maker (MM)** whose goal is to maximize the expected utility of terminal wealth while managing **inventory risk**.
*   **Utility Function:** CARA (Constant Absolute Risk Aversion) utility: $E[-\exp(-\gamma(X_T + q_TS_T))]$.
*   **Risk Parameter ($\gamma$):** Represents the trader's risk aversion. High $\gamma$ means the MM is more sensitive to price fluctuations and will move quotes more aggressively to revert inventory to zero.
*   **Inventory Limits ($Q$):** The strategy explicitly assumes a hard limit on inventory ($|q| \leq Q$).

### 2. Market Dynamics (Assumptions)
*   **Reference Price ($S_t$):** Follows an Arithmetic Brownian Motion: $dS_t = \sigma dW_t$.
*   **Order Arrival (Liquidity):** Modeled as a Poisson process where the probability of being filled depends on the distance from the mid-price ($\delta$).
    *   The intensity (fill rate) is $\lambda(\delta) = A e^{-k\delta}$.
    *   **$A$:** Frequency of market orders (liquidity).
    *   **$k$:** Sensitivity of execution to price (market depth/impact).

### 3. The Strategy Logic (Optimal Quotes)
The MM must decide the distance of the bid ($\delta^b$) and ask ($\delta^a$) from the reference price. The logic splits the quote into two components: **The "Indifference" Spread** and the **Inventory Skew**.

#### A. The General Solution
The optimal quotes at time $t$ for a given inventory $q$ are:
$$\delta^b(t, q) = \frac{1}{k} \ln \left( \frac{v_q(t)}{v_{q+1}(t)} \right) + \frac{1}{\gamma} \ln\left(1 + \frac{\gamma}{k}\right)$$
$$\delta^a(t, q) = \frac{1}{k} \ln \left( \frac{v_q(t)}{v_{q-1}(t)} \right) + \frac{1}{\gamma} \ln\left(1 + \frac{\gamma}{k}\right)$$
*Where $v_q(t)$ is a system of linear ODEs solved via matrix exponential of a tridiagonal matrix $M$.*

#### B. The Simplified Asymptotic Logic (Closed-Form)
For most of the trading day (when $t$ is far from $T$), the MM should follow this logic:
1.  **Fixed Spread Component:** The base spread is primarily determined by $\frac{2}{\gamma} \ln(1 + \frac{\gamma}{k})$.
2.  **Inventory Adjustment (Skewing):** The MM shifts both quotes to encourage trades that reduce inventory and discourage trades that increase it.
    *   **If Long ($q > 0$):** Increase $\delta^b$ (move bid lower, further from mid) and decrease $\delta^a$ (move ask lower, closer to mid). This makes it harder to buy more and easier to sell.
    *   **If Short ($q < 0$):** Decrease $\delta^b$ (move bid higher, closer to mid) and increase $\delta^a$ (move ask higher, further from mid). This makes it easier to buy and harder to sell.

#### C. Linear Approximation Formula
The paper provides a simplified rule of thumb for the quotes:
$$\delta^b_\infty(q) \approx \text{Base Spread} + \frac{2q+1}{2} \sqrt{\frac{\sigma^2 \gamma}{2kA} \left(1 + \frac{\gamma}{k}\right)^{1+k/\gamma}}$$
$$\delta^a_\infty(q) \approx \text{Base Spread} - \frac{2q-1}{2} \sqrt{\frac{\sigma^2 \gamma}{2kA} \left(1 + \frac{\gamma}{k}\right)^{1+k/\gamma}}$$

### 4. Logic Extensions
#### A. Price Trend (Drift $\mu$)
If the MM detects a trend ($dS_t = \mu dt + \sigma dW_t$):
*   The MM shifts the entire quote window in the direction of the trend to avoid being "picked off" and to accumulate position in anticipation of the move.

#### B. Market Impact / Adverse Selection ($\xi$)
If executions cause the mid-price to jump (Market Impact):
*   The MM increases the spread by $\xi$ (the impact parameter).
*   The logic accounts for the fact that every fill moves the market against the MM’s remaining position.

### 5. Summary Table of Variable Influences
| Parameter | Increase in Parameter | Effect on Strategy |
| :--- | :--- | :--- |
| **Volatility ($\sigma$)** | High | Increases the spread and the intensity of inventory skewing. |
| **Risk Aversion ($\gamma$)** | High | Increases the spread and makes the MM much more aggressive in reducing inventory. |
| **Liquidity ($A$)** | High | Decreases the spread (more competition/tighter market). |
| **Price Sensitivity ($k$)** | High | Decreases the spread (thinner book/higher impact of distance). |
| **Time to Horizon ($T-t$)** | High | Quotes remain stable; as $t \to T$, the inventory risk fades and quotes tighten. |

### 6. Key Takeaway for Implementation
The strategy logic effectively replaces complex PDE solvers with a **matrix diagonalization problem**. By pre-calculating the smallest eigenvalue and eigenvector of the matrix $M$, a trader can determine the optimal "inventory-neutral" quote and the "skew" factor per unit of inventory in real-time.