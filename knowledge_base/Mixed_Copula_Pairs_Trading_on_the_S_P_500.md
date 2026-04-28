This strategy, as outlined in the paper **"A Pairs Trading Strategy Based on Mixed Copulas"** (Sabino da Silva, Ziegelmann, and Caldeira, 2017), is a statistical arbitrage approach that improves upon the traditional "Distance Method" by using flexible copula models to capture complex, non-linear dependencies and tail risks between stocks.

Here is the extracted strategy logic:

### 1. The Core Philosophy
Traditional pairs trading (Distance Method) assumes that the spread between two stocks follows a symmetric, normal distribution. The authors argue that stock dependencies are often asymmetric (e.g., stocks crash together faster than they rise together). By using **Mixed Copulas**, the strategy can model different "tail dependencies" (upper and lower) simultaneously, allowing for more precise entries and exits.

---

### 2. Phase 1: Formation (Pair Selection)
*   **Lookback Period:** 12 months (Formation Period).
*   **Universe:** S&P 500 constituents.
*   **Selection Metric:** 
    1.  Normalize all stock prices to start at $1 at the beginning of the formation period.
    2.  Calculate the **Sum of Squared Deviations (SSD)** between normalized price series for all possible pairs.
    3.  Select the **Top $N$ pairs** (typically the top 5 to 35) with the minimum SSD.

---

### 3. Phase 2: Modeling (The Copula Engine)
Unlike the distance method, which looks at price spreads, the Copula method looks at the **joint distribution of returns**.

1.  **Marginal Distribution Modeling:** 
    *   Filter the daily returns of each stock in a pair using an **ARMA(p,q)-GARCH(1,1)** model. 
    *   This removes autocorrelation and volatility clustering, leaving "standardized residuals."
    *   Convert these residuals into uniform distributions $[0,1]$ using their Empirical Cumulative Distribution Function (ECDF).
2.  **The Mixed Copula Model:** 
    *   The strategy uses a weighted mixture of different copulas to capture various market states.
    *   **Mixture Equation:** $C_{mix} = w_1 \cdot C_{Clayton} + w_2 \cdot C_{Student-t} + (1 - w_1 - w_2) \cdot C_{Gumbel}$.
    *   *Clayton:* Captures lower tail dependence (crashing together).
    *   *Gumbel:* Captures upper tail dependence (rising together).
    *   *Student-t:* Captures symmetric extreme co-movements.
3.  **Parameter Estimation:** Estimate the weights ($w$) and parameters for each pair using Maximum Likelihood Estimation (MLE) based on the formation period data.

---

### 4. Phase 3: Trading Signals (The Mispricing Index)
The strategy calculates a **Mispricing Index (MI)** based on conditional probability.

*   **Conditional Probability:** It calculates the probability that stock $X$’s return should be less than or equal to its current value, given the return of stock $Y$.
*   **Mispricing Index (MI):** $MI_{X|Y} = P(R_X \leq r_x | R_Y = r_y)$.
    *   If $MI \approx 0.5$, the pair is in equilibrium.
    *   If $MI > 0.5$, stock $X$ is "expensive" relative to $Y$.
    *   If $MI < 0.5$, stock $X$ is "cheap" relative to $Y$.
*   **Cumulative Mispricing Index (CMI):** To filter noise, the authors track the *sum* of deviations from the mean (0.5) over time:
    $$M_{t} = M_{t-1} + (MI_{t} - 0.5)$$

---

### 5. Phase 4: Execution Logic
*   **Entry Signal:** 
    *   Open a trade when the CMIs of the two stocks diverge significantly.
    *   **Threshold:** Typically, when $M_{1,t} > 0.2$ and $M_{2,t} < -0.2$ (or vice versa).
    *   **Action:** Short the relatively overvalued stock and Long the relatively undervalued stock.
*   **Exit Signal:** 
    *   Close the position when the CMIs return to **zero** (convergence to the historical relationship).
    *   **Stop-Out:** Automatically close all positions at the end of the 6-month trading period.

---

### 6. Risk Management & Costs
*   **Trading Period:** 6 months (then re-evaluate and select new pairs).
*   **Weighting:** 
    *   *Committed Capital:* Capital is divided equally among the top $N$ selected pairs at the start.
    *   *Fully Invested:* Capital is divided only among the pairs currently "open."
*   **Transaction Costs:** The paper assumes 20 basis points (0.20%) per round-trip trade to ensure the results are realistic for institutional trading.

### Summary of Results
*   **Superiority:** The Mixed Copula approach (specifically the **CtG** - Clayton-t-Gumbel mixture) outperforms the Distance Method in Sharpe Ratio and Drawdown.
*   **Tail Risk:** Because it accounts for "lower tail dependence," the strategy performs better during market stress compared to simpler linear models.
*   **Alpha:** The returns are not fully explained by Fama-French factors, suggesting the strategy captures a unique statistical arbitrage premium.