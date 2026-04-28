Based on the paper *"A Primer on Alternative Risk Premia"* by Hamdan, Pavlowsky, Roncalli, and Zheng (2016), the strategy logic can be extracted and categorized into three main components: the core philosophy, the classification of the "Risk Factor Zoo," and the specific mechanics of individual strategies.

---

### 1. Core Philosophy: The "Bad Times" Theory
The paper defines Alternative Risk Premia (ARP) as systematic sources of return that go beyond traditional long-only exposure to equities and bonds. The fundamental logic for why these strategies work is rooted in two distinct theories:

*   **Risk-Based Logic (SDF Theory):** Premia exist as compensation for holding assets that perform poorly during "bad times" (recessions or market crashes). If an asset has a negative covariance with the Stochastic Discount Factor (SDF), investors demand a premium to hold it.
*   **Behavioral/Structural Logic:** Premia exist due to market anomalies, such as investor irrationality (e.g., herding in Momentum) or institutional constraints (e.g., the inability of many investors to use leverage, leading to the Low Beta anomaly).

### 2. The Binary Classification of ARP
The authors categorize all ARP into two functional groups based on their payoff profiles:

#### A. Skewness Risk Premia (Concave Payoffs)
*   **Logic:** These strategies act like "selling insurance." They collect small, steady premiums but are prone to rare, large drawdowns.
*   **Mathematical Profile:** Negative skewness.
*   **Examples:** Carry (FX, Rates), Short Volatility, and Value.
*   **Strategy Behavior:** Often mean-reverting. If the price of an asset drops, the strategy increases exposure (buying the dip), which increases risk during a total default or structural shift.

#### B. Market Anomalies (Convex Payoffs)
*   **Logic:** These exploit structural inefficiencies or behavioral biases. They do not necessarily crash during "bad times."
*   **Mathematical Profile:** Positive or neutral skewness.
*   **Examples:** Momentum (Trend-following), Quality, and Low Volatility.
*   **Strategy Behavior:** Often trend-following. If an asset price drops, the strategy reduces exposure or goes short, providing a form of "convexity" that can protect the portfolio during sustained crashes.

---

### 3. Strategy-Specific Logic
The paper details the mechanics for the most common ARP factors:

| Strategy | Asset Classes | Underlying Logic / Mechanic |
| :--- | :--- | :--- |
| **Carry** | FX, Rates, Credit, Commodities | **Logic:** Exploiting the difference between the spot price and the forward/future price. **Mechanic:** Long high-yielding assets and short low-yielding assets. |
| **Value** | Equities, FX, Commodities | **Logic:** Mean-reversion to fundamental value. **Mechanic:** Long "cheap" assets (high book-to-market, low P/E) and short "expensive" assets. |
| **Momentum** | All | **Logic:** Behavioral under-reaction/over-reaction to news. **Mechanic:** Long recent winners and short recent losers (Trend-following). |
| **Low Beta / Vol** | Equities | **Logic:** Leverage aversion. Investors overpay for high-beta stocks to get "lottery-like" returns because they cannot use margin. **Mechanic:** Long low-volatility stocks, short high-volatility stocks. |
| **Quality** | Equities | **Logic:** Profitable, low-debt, and stable companies are often undervalued by the market. **Mechanic:** Long high-quality firms, short low-quality "junk" firms. |
| **Size** | Equities | **Logic:** Compensation for liquidity risk and higher distress risk in small-cap companies. **Mechanic:** Long small-cap, short large-cap. |

---

### 4. Implementation and Portfolio Logic
The paper introduces several critical logic points for constructing an ARP portfolio:

*   **Beyond Volatility Parity:** Traditional risk parity (weighting by inverse volatility) is insufficient for ARP because it ignores **tail risk**. Since many ARP have high negative skewness (like Carry), a portfolio balanced by volatility alone will be dangerously over-exposed to "jump" risks.
*   **The Lasso Regression for Alpha Decomposition:** The authors use a Lasso (L1-regularized) regression model to analyze hedge fund returns.
    *   **Logic:** Most hedge fund "Alpha" is actually "Alternative Beta."
    *   **Finding:** When traditional factors (Equity/Credit) are combined with ARP factors, many hedge fund strategies' alphas disappear, proving they are simply harvesting these systematic alternative premia.
*   **Diversification of Payoffs:** A robust portfolio should mix **Skewness Premia** (which perform well in stable markets) with **Market Anomalies** (like Momentum, which can perform well during high-volatility trending markets).

### 5. Summary of Key Findings
*   **Alternative Beta:** ARP are the building blocks of hedge fund returns.
*   **Complexity of Aggregation:** Diversifying 50+ risk premia is harder than diversifying stocks because their correlations increase during "bad times" (correlation of the tails).
*   **Generic Indices:** The paper suggests that ARP can be effectively captured using liquid, transparent commercial indices rather than high-fee active managers.