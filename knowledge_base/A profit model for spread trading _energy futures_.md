Based on the paper "A profit model for spread trading with an application to energy futures" by Kanamura, Rachev, and Fabozzi (2011), the strategy logic can be extracted and categorized into its mathematical foundation, execution rules, and market-specific applications.

### 1. Core Philosophy: Statistical Arbitrage
The strategy is a form of **"Pairs Trading"** or **"Convergence Trading."** It assumes that the price spread between two highly correlated assets (in this case, energy futures of different maturities or types) is stationary and will eventually revert to a long-term mean. Profit is generated from the relative movement of the two prices rather than the direction of the overall market.

---

### 2. Mathematical Foundation: The Mean-Reverting Model
The authors model the price spread ($S_t$) using an **Ornstein-Uhlenbeck (OU) process**:

$$dS_t = \kappa(\theta - S_t)dt + \sigma dW_t$$

*   **$\kappa$ (Kappa):** The speed of mean reversion.
*   **$\theta$ (Theta):** The long-term mean of the spread.
*   **$\sigma$ (Sigma):** The volatility of the spread.
*   **$dW_t$:** A Wiener process (random noise).

**The Innovation:** The paper uses the **First Hitting Time (FHT)** probability density. It calculates the expected profit based on two scenarios:
1.  **Convergence:** The spread hits the target (usually 0 or the mean) before the trading period ends.
2.  **Failure to Converge:** The spread does not hit the target by time $T$, and the position is forced closed at the current market spread.

---

### 3. Strategy Execution Logic (Empirical Setup)

The authors use a "Formation Period" to select pairs and a "Trading Period" to execute.

#### A. Formation Phase (Selection)
*   **Duration:** 120 trading days.
*   **Pair Selection:** Calculate the spread for all possible combinations of futures.
*   **Criterion:** Select the pair with the **smallest standard deviation** of price spreads during this period.
*   **Normalization:** Prices are normalized so that the first day of the period starts at the same level (cumulative returns).

#### B. Trading Phase (Execution)
*   **Duration:** 120 trading days (immediately following the formation period).
*   **Entry Signal:** Open a "zero-cost" portfolio when the spread deviates from the mean by **more than 2 standard deviations ($2\sigma$)**.
    *   **Action:** Short the overpriced asset and Long the underpriced asset.
*   **Exit Signal (Profit):** Close the positions if the price spread converges (returns to the mean).
*   **Exit Signal (Stop/End):** Close all positions at the end of the 120-day trading period, regardless of convergence.

---

### 4. Key Profitability Determinants
The paper identifies three primary factors that drive the success of this strategy:

1.  **Speed of Mean Reversion ($\kappa$):** Higher $\kappa$ results in faster convergence, allowing for more frequent trades and higher turnover.
2.  **Volatility ($\sigma$):** Higher volatility increases the probability that the spread will hit the entry threshold and subsequently "snap back" to the mean.
3.  **Seasonality:** In energy markets (Heating Oil and Natural Gas), seasonality significantly impacts spread behavior. The authors found higher profitability during winter months.

---

### 5. Application to Energy Futures
The paper specifically tests the strategy on NYMEX WTI Crude Oil, Heating Oil (HO), and Natural Gas (NG).

*   **Natural Gas (NG) Findings:** Produced the highest expected returns. This is attributed to NG's **exceptionally high volatility** and **strong mean-reversion speed** compared to WTI or HO.
*   **Seasonality Bias:**
    *   **WTI:** Profitability is relatively stable across seasons.
    *   **HO & NG:** Higher profits in "Winter Trades" (December–February). NG also showed high profitability in "Fall Trades" (September–October).
*   **Market Efficiency:** The consistent profitability of this strategy suggests that energy futures markets exhibit temporary inefficiencies that can be exploited by mean-reversion traders.

### Summary for Implementation
To replicate this strategy:
1.  Identify two correlated energy futures (e.g., 1-month vs. 2-month Natural Gas).
2.  Calculate the historical standard deviation of their spread over the last 120 days.
3.  Sell the spread when it widens beyond $2\sigma$.
4.  Buy the spread back when it returns to its mean.
5.  Prioritize assets with high volatility and fast mean-reversion speeds (like Natural Gas) and focus on periods of high seasonal demand.