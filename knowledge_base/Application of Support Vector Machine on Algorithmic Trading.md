Based on the paper **"Application of Support Vector Machine on Algorithmic Trading"** by Szklarz et al., the strategy logic can be extracted and categorized as follows:

### 1. Strategy Concept
The core innovation of this strategy is the use of **separated training models** for different market regimes. Instead of one general model, the authors develop distinct Support Vector Machine (SVM) models for **up-trending** and **down-trending** periods. The strategy focuses on the **S&P 500** index, leveraging its inverse correlation with the **VIX** (Volatility Index).

---

### 2. Input Features (The "X" Variables)
The models use 10 quantitative inputs derived from price data and volatility:
1.  **RSI (14 periods):** Current day's close.
2.  **RSI (14 periods):** Previous day’s close.
3.  **RSI (14 periods):** Two days ago close.
4.  **MACD (26, 12, 9):** Current day's close.
5.  **MACD (26, 12, 9):** Previous day’s close.
6.  **MACD (26, 12, 9):** Two days ago close.
7.  **VIX Index:** Current close.
8.  **VIX Index:** Previous day’s close.
9.  **VIX Index:** Two days ago close.
10. **S&P 500 % Change:** Current close.

---

### 3. Training Logic (The "Target" or Labels)
To train the machine learning models, the "ground truth" (expected output) is defined by a 5-day forward-looking window:
*   **Buy Signal (+1):** Generated if the price 5 days in the future is higher than today’s price.
*   **Sell Signal (-1):** Generated if the price 5 days in the future is lower than today’s price.

---

### 4. The SVM Model Configuration
The strategy utilizes a specific variation of SVM:
*   **Algorithm:** SVM-KM (SVM combined with K-means clustering to identify and remove outliers/non-useful data).
*   **Kernel:** High Tail Radial Basis Function (HTRBF).
*   **Hyperparameters:** $C = 100$, $\lambda = 0.0000001$.
*   **Output:** The model produces a vector in the range of $[-1, 1]$, representing the "degree of belonging" to a class (Purchase or Sale).

---

### 5. Execution Logic (Backtesting Rules)
The strategy is designed for mid-term trading with the following execution constraints:
*   **Regime-Specific Trading:**
    *   **In Up-trending Markets:** The system only executes **Long** (purchase) operations. Only one operation can be open at a time.
    *   **In Down-trending Markets:** The system only executes **Short** (sale) operations. Only one operation can be open at a time.
*   **Position Sizing:** 100% of available capital is used for each trade.
*   **Transaction Costs:** 0.35% commission per operation is factored into the logic.

---

### 6. Post-Filtering & Optimization
After the SVM generates a signal, two optional filters are applied to refine the entries:
1.  **Gain / Stop Loss (G/SL):**
    *   Cancels an exit signal if a minimum gain hasn't been reached.
    *   Triggers an immediate exit (Stop Loss) if the price drops below a fixed percentage, regardless of the SVM signal.
2.  **ADX Filter (Average Directional Index):**
    *   Uses a 14-period ADX to measure trend strength.
    *   If the trend strength is below a specific threshold, the trade is cancelled (filtering out sideways/choppy markets).

---

### 7. Key Findings & Performance
*   **Up-trend Performance:** The SVM performed well but struggled to beat a simple "Buy and Hold" strategy.
*   **Down-trend Performance:** This is where the SVM logic excelled. It significantly outperformed quantitative indicators (RSI, MACD) and other ML methods (Random Forest, Naïve-Bayes). 
*   **VIX Relevance:** Including VIX data was found to be critical for the accuracy of the SVM, particularly in predicting market reversals during down-trending periods.
*   **Best Filter:** The **Stop Loss** filter was found to be the most effective addition to the SVM logic for protecting capital.