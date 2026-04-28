Based on the paper "Hidden Markov Model for Stock Selection" (2015) by Nguyen and Nguyen, the strategy logic can be extracted and summarized into the following operational steps:

### 1. Core Philosophy
The strategy is based on the premise that stock returns and the effectiveness of specific stock characteristics (factors) vary significantly across different macroeconomic "regimes." By using a Hidden Markov Model (HMM) to forecast the upcoming economic regime, the strategy identifies which stock factors have historically performed best in that specific environment and selects stocks that rank highest in those factors.

---

### 2. Input Variables
The model utilizes two distinct sets of data:

**A. Macroeconomic Indicators (for Regime Detection):**
*   **Inflation:** 12-month changes in the Consumer Price Index (CPI).
*   **Industrial Production:** Monthly changes in the Industrial Production Index (INDPRO).
*   **Market Return:** One-month changes in the S&P 500 Index.
*   **Market Volatility:** Levels of the CBOE Volatility Index (VIX).

**B. Stock Characteristics/Factors (for Stock Selection):**
1.  **Earnings/Price (E/P):** Valuation yield.
2.  **Free Cash Flow/Enterprise Value (FCF/EV):** Valuation yield.
3.  **Sales/Enterprise Value (S/EV):** Valuation yield.
4.  **Long-term EPS Growth:** 5-year moving regression trend of earnings per share.
5.  **Long-term Sales Growth:** 5-year moving regression trend of sales.

---

### 3. The Strategy Logic (Step-by-Step)

#### Step 1: Regime Calibration and Prediction
At the end of each month, the model calibrates an HMM for each of the four macroeconomic indicators. 
*   **States:** Each indicator is modeled with **two states** (e.g., Bull vs. Bear market, Growth vs. Recession, Inflation vs. Deflation).
*   **Algorithm:** The **Baum-Welch algorithm** is used to calibrate the HMM parameters ($\lambda$), and the **Viterbi algorithm** is used to determine the most likely hidden state (regime) for the upcoming month.

#### Step 2: Historical Pattern Matching
Once the next month's regimes for the four indicators are predicted, the model looks back through 20 years of historical data to find specific months where the macro-environment matched the predicted state combination (e.g., months where CPI was in State 1, INDPRO in State 2, etc.).

#### Step 3: Factor Performance Attribution
Within those matching historical periods, the model evaluates the performance of the five stock factors listed above. It calculates which factors were the most rewarded (generated the highest returns).

#### Step 4: Scoring and Weighting
*   **Rank Factors:** The five factors are ranked (1 to 5) based on their historical performance during the identified regimes.
*   **Assign Weights:** Weights are assigned to each factor based on its rank (Factor Rank / Sum of all Ranks).
*   **Composite Stock Score:** Every stock in the S&P 500 universe is assigned a composite score:
    $$\text{Composite Score} = \sum (\text{Factor Score} \times \text{Factor Weight})$$
*   Scores are scaled from 1 to 100.

#### Step 5: Portfolio Construction
*   **Selection:** The top 50 ranking stocks (the top decile) by composite score are selected for the portfolio.
*   **Rebalancing:** The process is repeated **monthly**. If a stock no longer appears in the top 50, it is sold and replaced by a new entrant.

---

### 4. Key Performance Results (1999–2014)
*   **Annualized Return:** 14.9% (Portfolio) vs. 2.3% (S&P 500).
*   **Risk Profile:** The portfolio showed a higher Sharpe Ratio (0.61) than individual factor strategies, suggesting that switching factor weights based on HMM regimes provides better risk-adjusted returns through diversification.
*   **Turnover:** The average holding period for a stock in the portfolio is approximately three months.

### 5. Summary of Mathematical Tools
*   **HMM Parameters:** $\lambda = \{A, B, \pi\}$ (Transition matrix, Observation matrix, Initial probability).
*   **Estimation:** Maximum Likelihood Estimation (MLE) via Baum-Welch.
*   **State Determination:** Viterbi Algorithm.
*   **Distribution:** Gaussian (Normal) distribution assumed for the observation probabilities of the macro variables.