Based on the research paper "Predicting the direction of stock market prices using random forest" by Khaidem, Saha, and Dey, the strategy logic can be extracted and organized into the following components:

### 1. Core Philosophy
The strategy treats stock market forecasting as a **binary classification problem** rather than a regression problem. Instead of predicting the exact price, it predicts the **direction of the trend** (Rise or Fall) over a specific time horizon. This approach aims to minimize forecasting errors and market risk.

### 2. Data Preprocessing (Noise Reduction)
Before feature extraction, the raw historical price data is smoothed to remove "noise" (random fluctuations) and identify long-term trends.
*   **Method:** Exponential Smoothing.
*   **Formula:** $S_t = \alpha \cdot Y_t + (1 - \alpha) \cdot S_{t-1}$
*   **Logic:** Recent observations are weighted more heavily, but the inclusion of past observations creates a smoother series for the algorithm to learn from.

### 3. Feature Engineering (Technical Indicators)
The model uses six key technical indicators as inputs (features) to capture momentum, trend, and volume:

1.  **Relative Strength Index (RSI):** Measures momentum and identifies overbought (>70) or oversold (<30) conditions.
2.  **Stochastic Oscillator (%K):** Compares a specific closing price to a range of its prices over a 14-day period.
3.  **Williams %R:** A momentum indicator that measures overbought and oversold levels, specifically looking at the high-low range.
4.  **Moving Average Convergence Divergence (MACD):** A trend-following momentum indicator showing the relationship between two moving averages of prices.
5.  **Price Rate of Change (PROC):** Measures the percentage change in price between the current period and $n$ periods ago.
6.  **On Balance Volume (OBV):** Uses volume flow to predict changes in stock price (momentum indicator).

### 4. Target Labeling (The Prediction Goal)
The strategy defines the target variable based on a future time window ($d$ days).
*   **Target Logic:** $target_i = Sign(Close_{i+d} - Close_i)$
*   **Labels:**
    *   **+1 (Rise):** If the price after $d$ days is higher than today’s price.
    *   **-1 (Fall):** If the price after $d$ days is lower than today’s price.
*   **Time Horizons Tested:** 30 days, 60 days, and 90 days.

### 5. Machine Learning Model: Random Forest
The core engine is a **Random Forest Classifier**, an ensemble of multiple Decision Trees.
*   **Training Method:** Bagging (Bootstrap Aggregating). It trains multiple trees on different random subsets of the data and features.
*   **Decision Logic:** Each tree in the forest "votes" on whether the stock will rise or fall. The final prediction is the **mode** (majority vote) of all trees.
*   **Splitting Criterion:** Uses **Gini Impurity** or **Shannon Entropy** to determine the best way to split data at each node of the trees.
*   **Advantage:** This model handles non-linear relationships and is robust against overfitting compared to a single decision tree.

### 6. Execution Logic (Trading Rules)
Based on the model's output, the investment decision is straightforward:
*   **Buy Signal:** If the Random Forest output is **+1**, the model expects the price to be higher in $d$ days.
*   **Sell/Refrain Signal:** If the Random Forest output is **-1**, the model expects the price to be lower in $d$ days.

### 7. Key Findings & Performance Logic
*   **Linear Separability:** The authors used Convex Hull tests to prove that stock data is **not linearly separable**, justifying the use of complex non-linear models like Random Forest over simpler models like Linear Discriminant Analysis.
*   **Convergence:** The Out-of-Bag (OOB) error decreases as the number of trees increases, meaning the model becomes more stable and accurate as the ensemble grows.
*   **Time Horizon Correlation:** The model's accuracy **increases** as the prediction window ($d$) gets longer. 
    *   *Example (Apple Data):* Accuracy was ~88% for 30 days, but improved to ~94.5% for 90 days.
*   **Accuracy:** The model consistently achieved 85% to 95% accuracy across different markets (NASDAQ, Korean Stock Exchange).