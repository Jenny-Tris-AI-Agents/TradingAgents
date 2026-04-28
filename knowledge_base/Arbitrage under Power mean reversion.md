Based on the paper **"Arbitrage under Power"** by Michael Boguslavsky and Elena Boguslavskaya, the following is the extracted strategy logic.

---

### 1. Strategy Objective
The strategy seeks to determine the **optimal position size** ($\alpha$) for a trader with limited capital and a finite time horizon who is trading a **mean-reverting asset** (such as a cointegrated pair or a spread). The goal is to maximize the **Expected Power Utility** of terminal wealth.

### 2. Market Model (The "Setup")
*   **Asset Dynamics:** The asset price (or spread) $X_t$ follows an **Ornstein-Uhlenbeck (OU) process**:
    $$dX_t = -kX_t dt + \sigma dB_t$$
    *   $k$: Speed of mean reversion.
    *   $\sigma$: Volatility/Noise.
    *   Long-term mean is assumed to be $0$.
*   **Utility Function:** The trader uses **Power Utility**: $U(W) = \frac{1}{\gamma}W^\gamma$.
    *   The relative risk aversion is $1 - \gamma$.
    *   $\gamma < 1$ (where $\gamma \to 0$ represents Log-Utility).

### 3. The Optimal Trading Rule
The optimal number of units ($\alpha^*$) to hold at any time $t$ is defined by:
$$\alpha^*_t = -W_t \cdot X_t \cdot D(\tau)$$

**Components of the formula:**
*   $W_t$: Current wealth (the strategy is self-financing and scales with capital).
*   $X_t$: Current value of the spread (tells you the direction: short if positive, long if negative).
*   $D(\tau)$: A time-dependent function that accounts for risk aversion and the time remaining ($\tau = T - t$).

**Calculation of $D(\tau)$:**
1.  Define $\nu = 1/\sqrt{1-\gamma}$.
2.  Define $C(\tau) = \cosh(\nu \tau) + \nu \sinh(\nu \tau)$.
3.  Define $C'(\tau) = \nu \sinh(\nu \tau) + \nu^2 \cosh(\nu \tau)$.
4.  $D(\tau) = C'(\tau) / C(\tau)$.

### 4. Position Management Logic
The paper identifies non-trivial qualitative behaviors for managing the position:

*   **Scaling In:** As the spread ($X_t$) moves away from the mean, the trader increases the position size.
*   **The "Cutting Point" (Stop Loss Logic):** Unlike a naive strategy that holds indefinitely, this model dictates a point where the trader should **cut the position** even if the spread continues to widen.
    *   **Condition:** If $|X| > \sqrt{1/D(\tau)}$, the trader starts cutting the loss-making position.
    *   **Interpretation:** This happens when the unrealized loss on the spread exceeds the total wealth ($-\alpha X > W$).
*   **Time Sensitivity:**
    *   **Risk Averse ($\gamma < 0$):** As the time horizon ($T$) approaches (e.g., year-end), the trader becomes **less aggressive** and reduces position size.
    *   **Less Risk Averse ($\gamma > 0$):** The trader becomes **more aggressive** as the horizon approaches, taking larger bets to maximize terminal utility.
    *   **Log-Utility ($\gamma = 0$):** The strategy is time-independent; the trader doesn't care how much time is left.

### 5. Risk and Parameter Sensitivity
*   **Mean Reversion ($k$):** Higher speed of mean reversion ($k$) allows for more aggressive positioning.
*   **Volatility ($\sigma$):** Higher noise/volatility requires a smaller position size.
*   **Parameter Uncertainty (The "Conservative" Rule):**
    *   It is safer to **underestimate** the speed of mean reversion ($k$). Overestimating $k$ leads to over-leveraging and potential ruin.
    *   It is safer to **overestimate** the noise ($\sigma$) than to underestimate it.

### 6. Summary of Qualitative Effects
| Scenario | Strategy Action |
| :--- | :--- |
| **Spread widens slightly** | Increase position size (averaging in). |
| **Spread widens extremely** | Decrease position size (cutting losses/risk management). |
| **Approaching year-end (Risk Averse)** | Reduce position size to "lock in" or protect capital. |
| **Approaching year-end (Aggressive)** | Increase position size to maximize potential gain. |
| **Wealth increases** | Increase position size (constant relative risk aversion). |

### 7. Implementation Note
The position is linear in both wealth and the spread ($ \alpha \propto W \cdot X $). This means the strategy effectively suggests a **constant leverage** relative to the distance from the mean, adjusted by the time-to-horizon factor $D(\tau)$.