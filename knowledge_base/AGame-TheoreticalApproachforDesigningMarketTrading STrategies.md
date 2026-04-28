Based on the paper "A Game-Theoretical Approach for Designing Market Trading Strategies," the strategy logic can be decomposed into four primary components: the **Market Target**, the **Technical Features**, the **Fuzzy Inference System**, and the **Co-evolutionary Learning Mechanism**.

---

### 1. The Market Target: "Trend Days"
The strategy does not attempt to predict exact prices. Instead, it aims to identify **Up-Trend Days**. 
*   **Up-Trend Day Definition:** 
    *   Opening price ($O$) is near the day's low ($L$): $O \le L + 0.1(H - L)$
    *   Closing price ($C$) is near the day's high ($H$): $C \ge H - 0.2(H - L)$
*   **Goal:** Buy at the market open and sell at the market close on predicted trend days.

### 2. Input Technical Features
The system looks at historical data (Today = $i=0$) to identify features that typically precede a trend day:

*   **Narrow Range ($NRk$):** Today’s range ($H-L$) is the smallest of the previous $k$ days. This represents "volatility contraction" which often leads to "volatility expansion." (The paper uses $k = 4, 6, 7$).
*   **DOJI:** The open and close prices are within a very small percentage ($x$) of each other, signaling market indecision or a pending reversal.
*   **Hook Day:** The price opens outside the previous day’s range and then reverses direction, signaling a reaction to overbought/oversold conditions.

### 3. Fuzzy Logic Framework
The authors argue that "crisp" rules (e.g., "If NR7 is True, then Buy") are too rigid. They use fuzzy membership functions to handle "partial" forms of these features.

*   **Fuzzification:** Instead of a binary Yes/No, features are assigned a membership value between 0 and 1. For example, if a day is *almost* a DOJI, it might receive a value of 0.8.
*   **The Rule-Base (Matrix $M$):** The strategy is stored as a matrix where rows are features and columns are "Buy Desirability" singletons ($0.25, 0.5, 0.75, 1.0$). 
*   **Inference:** The system calculates the dot product of the input feature vector ($A$) and the strategy matrix ($M$) using the Max-Min composition.
*   **Defuzzification:** The resulting fuzzy output is converted into a crisp "Desirability" score ($U$) between 0 and 1.

### 4. Execution Logic
*   **The Threshold:** A trade is only executed if the Desirability Score $U > 0.8$.
*   **Position Sizing:** The amount of stock purchased increases linearly as $U$ increases from 0.8 toward 1.0 (up to a maximum of 20 shares).
*   **Trade Timing:** Enter at Open ($O$), Exit at Close ($C$). All proceeds are deposited back into a bank account daily.

### 5. Strategy Evolution (Game Theory)
The logic is not "hand-coded" but evolved using a game-theoretical approach to ensure robustness:

*   **Competitive Co-evolution:** Two "brokerage firms" ($\alpha$ and $\omega$) evolve independent populations of strategies.
*   **Zero-Sum Game:** Strategies are evaluated in tournaments. When a strategy from Firm $\alpha$ outperforms a strategy from Firm $\omega$ over a 150-day window, the winner "takes" 2% of the loser's bank account balance. 
*   **Fitness:** "True fitness" is defined by the ability to attract/take dollars from competitors, rather than just absolute returns. This mimics real-world market competition.
*   **Optimization:** A (40 + 40) Evolution Strategy uses crossover and Gaussian mutation to refine the weights in the Matrix $M$.

### Summary of the Strategy Cycle
1.  **Analyze** the last $k$ days of data for NRk, DOJI, and Hook Day features.
2.  **Calculate** fuzzy membership values for those features.
3.  **Process** through the evolved Rule-Base Matrix.
4.  **Buy** at the open if the resulting score is $>0.8$.
5.  **Sell** at the close of the same day.
6.  **Update** the strategy via co-evolution based on performance relative to other "firms."