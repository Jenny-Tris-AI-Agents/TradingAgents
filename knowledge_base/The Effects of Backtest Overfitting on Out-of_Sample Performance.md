The paper **"Pseudo-Mathematics and Financial Charlatanism"** does not provide a "winning" investment strategy. Instead, it provides the **mathematical logic used to debunk overfitted strategies.** Its core logic focuses on how the number of trials ($N$) conducted during the research phase dictates the validity of a backtest.

Here is the strategy logic extracted from the paper, categorized by its mathematical and procedural components:

### 1. The Logic of "Selection Bias" (The Researcher's Path)
The authors argue that the more variations of a strategy you test (trials), the more likely you are to find a high Sharpe Ratio (SR) by pure chance.
*   **The Problem:** Most researchers only report the "optimal" version of a strategy and hide the hundreds or thousands of failed trials.
*   **The Logic:** Even if every strategy tested has an expected return of zero (pure noise), the maximum Sharpe Ratio found among $N$ trials will increase as $N$ increases.
*   **Mathematical Approximation:** The expected maximum Sharpe Ratio among $N$ independent trials is approximately:
    $$E[\max_N] \approx \sqrt{2 \ln[N]}$$
    *Example:* If you test 100 random, skill-less versions of a strategy, you are expected to find one with a Sharpe Ratio of roughly 3.0 just by luck.

### 2. Minimum Backtest Length (MinBTL) Logic
The paper introduces a formula to determine how much historical data is required to justify the number of trials performed.
*   **The Logic:** To prevent overfitting, the length of the backtest ($T$) must increase proportionally to the number of trials ($N$).
*   **The Formula:** 
    $$\text{MinBTL} \approx \left( \frac{\text{Expected Max SR IS}}{\text{Target SR}} \right)^2$$
*   **Strategic Requirement:** A researcher must report $N$ (the number of trials) to allow an investor to calculate if the backtest is long enough to be statistically significant. If $N$ is not reported, the backtest should be considered a "fraud."

### 3. The Logic of "Compensation Effects" (Why Overfitting Fails OOS)
The paper explains why overfitted strategies don’t just perform poorly—they often perform **negatively** out-of-sample (OOS).
*   **The Global Constraint Logic:** If a strategy is optimized against a dataset that has a "global constraint" (like a fixed mean or a long-term equilibrium), picking the best-performing path In-Sample (IS) guarantees picking a path that has "over-extended" itself. 
*   **Serial Correlation Logic:** Most financial series have "memory" (mean reversion). 
    *   **Logic:** If the IS performance is significantly above the mean due to overfitting, the OOS performance is mathematically likely to be negative as the process reverts to its equilibrium.
    *   **Conclusion:** In the presence of memory, backtest optimization is not just neutral; it is actively detrimental to future performance.

### 4. Logic of Model Complexity
The paper critiques the use of "filters" (stop-losses, entry thresholds, risk sizing) as a way to increase $N$ without the researcher realizing it.
*   **The Logic:** Every parameter added (e.g., "only buy on Tuesdays," "exit if down 2%") exponentially increases the number of potential model configurations. 
*   **The "Elephant" Principle:** With enough parameters, a researcher can "fit an elephant" (make a model fit any historical data perfectly), but it loses all predictive power for the future.

### 5. Practical Example: Seasonal Strategy Logic
The paper demonstrates the "Charlatanism" of seasonal strategies (e.g., "The Santa Claus Rally" or "Monday Effects").
*   **The Logic Test:**
    1.  Take a random walk (pure noise).
    2.  Define four parameters: Entry Day, Holding Period, Stop Loss, and Side (Long/Short).
    3.  Create a mesh of 8,800 possible combinations.
    4.  **Result:** Even on pure noise, this process will reliably produce a strategy with a Sharpe Ratio > 1.25. 
*   **Warning:** Just because a strategy has a "Probabilistic Sharpe Ratio" (PSR) that says the result is not zero, doesn't mean it's good; the PSR is invalidated if the researcher does not account for the 8,800 trials conducted to find it.

### Summary of Strategy "Red Flags"
Based on the paper’s logic, an investment strategy is likely "Pseudo-Mathematics" if:
1.  It reports high In-Sample (IS) performance but does not state how many variations ($N$) were tested.
2.  The backtest length is short relative to the number of parameters.
3.  The strategy relies on complex "technical analysis" filters (Fibonacci ratios, Elliott waves) that increase the trial count without a theoretical basis.
4.  The strategy claims to have found a "seasonal" pattern without providing a structural economic reason why that pattern exists.