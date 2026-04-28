Based on the text provided, the **Frequency Arbitrage** strategy exploits the empirical observation that historical volatility changes depending on how often you sample the data (the "Frequencygram"). 

In the case of the S&P 500 (SPX), **Daily Volatility is typically higher than Weekly Volatility.** This implies that prices tend to "mean revert" within the span of a week—they move around significantly day-to-day but end the week closer to where they started than a random walk would suggest.

Here is the extracted strategy logic:

### 1. The Core Hypothesis
*   **Observation:** Historical Volatility (Daily) $>$ Historical Volatility (Weekly).
*   **Inference:** There is "noise" or mean-reverting behavior at the intra-week level that disappears when looking at weekly snapshots.
*   **Goal:** Capture the spread between these two volatilities without taking directional risk or necessarily paying for option optionality (implied vol).

### 2. Theoretical Derivation (The Synthetic Approach)
To capture this spread using options, one would theoretically:
1.  **Buy** a strip of options and **delta-hedge daily**. (This profits if daily realized vol is high).
2.  **Sell** the same strip of options and **delta-hedge weekly**. (This profits if weekly realized vol is low).
3.  **Result:** The "Option" part (the cost/premium) cancels out. What remains is a pure "spot strategy" based on the difference in hedging frequencies.

### 3. The Actionable Spot Strategy (Intra-week Mean Reversion)
The paper simplifies the complex option hedging into a mathematical "Spot Strategy" that can be traded directly in the underlying index (e.g., SPX futures) without using options at all.

**The Strategy Rule:**
At any day $j$ during week $i$, maintain a position (exposure) in the index based on the following logic:

$$Position = \alpha \left( \frac{1}{S_{i,1}} - \frac{1}{S_{i,j}} \right)$$

*   **$S_{i,1}$**: The price of the index at the **start** of the current week.
*   **$S_{i,j}$**: The **current** price of the index on day $j$.
*   **$\alpha$**: A constant scale factor representing the dollar amount to be "invested" or the risk appetite.

### 4. How the Logic Operates
*   **Initial State:** At the start of the week ($S_{i,j} = S_{i,1}$), the position is zero.
*   **If Price Rises:** If the index moves up during the week ($S_{i,j} > S_{i,1}$), the term $(1/S_{start} - 1/S_{now})$ becomes **positive**. You increase your long exposure as the price rises.
*   **If Price Falls:** If the index moves down ($S_{i,j} < S_{i,1}$), the term becomes **negative**. You increase your short exposure as the price falls.
*   **The Mean Reversion Mechanism:** While the formula looks like "momentum" (buying as it goes up), it is actually designed to capture the **gamma spread**. Because you are betting that Daily Vol > Weekly Vol, you are effectively "Long Daily Gamma." 
*   **Profit Taking:** You profit if the index fluctuates wildly during the week (allowing you to buy low and sell high via daily rebalancing) but ends the week near its starting point (minimizing the "weekly" move).

### 5. Summary of Execution
1.  **Monday Open:** Note the starting price ($S_{i,1}$). Position is 0.
2.  **Daily (Tuesday–Friday):** Calculate the current deviation from the Monday price. 
3.  **Adjust Exposure:** Update your position in the index according to the $\alpha(1/S_{start} - 1/S_{now})$ formula.
4.  **Friday Close:** Close all positions. 
5.  **Repeat:** Start fresh the following Monday.

### Economic Intuition
This strategy essentially "harvests" the path-dependency of the index. It pays off if the **realized path** (daily steps) is much longer than the **net displacement** (weekly step). It is a way to trade "Relative Volatility" (Daily vs. Weekly) rather than "Absolute Volatility" (Realized vs. Implied).