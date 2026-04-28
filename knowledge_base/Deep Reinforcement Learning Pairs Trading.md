Based on the research paper by Andrew Brim, the strategy logic for the **Deep Reinforcement Learning (DRL) Pairs Trading** system can be broken down into the following key components:

### 1. Universe Selection (Pair Identification)
The strategy does not trade all stocks; it uses a two-step statistical filtering process to find "tradable" pairs from the S&P 500:
*   **Cointegration Test:** From 78,000 possible combinations, only those with an **Augmented Dickey-Fuller (ADF) p-value between 0 and 0.05** are selected. This ensures the spread between the two stocks is mean-reverting.
*   **Volatility Filter:** To ensure there is enough price movement to profit, the pair must have a **coefficient of variation (Standard Deviation / Mean) of 0.5 or greater.**
*   **Final Universe:** In this study, these filters reduced the field to **38 specific stock pairs**.

### 2. State Space (Input Features)
The DQN does not look at raw stock prices. Instead, it uses **10 derived features** that describe the relationship between the two stocks (the "spread"):
1.  Current spread of the pair.
2.  Daily returns of the spread.
3.  Spread mean for various time intervals (up to 15 days).
4.  The ratio of **Spread / Spread Mean** for those intervals (a ratio of 1.0 means equilibrium; 1.05 suggests the spread is high/overvalued; 0.95 suggests it is low/undervalued).

### 3. Action Space
For any given state, the agent can choose one of three actions:
*   **Long the Spread:** Simultaneously buy the lower-priced stock and sell the higher-priced stock.
*   **Short the Spread:** Simultaneously sell the lower-priced stock and buy the higher-priced stock.
*   **No Position:** Exit all positions or stay out of the market (reward is 0).

### 4. Reward Logic & The "Negative Multiplier"
The agent’s goal is to maximize cumulative rewards. The reward function is defined as:
$$\text{Reward} = \text{Action} \times \text{Spread Returns} \times \text{Negative Returns Multiplier}$$

*   **The Innovation:** The author introduces a **Negative Returns Multiplier** (ranging from 1 to 1000) during training.
*   **Logic:** By multiplying losses by a large factor, the agent is "punished" heavily for wrong trades. This forces the DQN to become **conservative**, choosing "No Position" unless it is highly confident, thereby increasing the win rate and reducing drawdowns.

### 5. Model Architecture (DQN)
The system utilizes a Deep Q-Network to approximate the optimal trading policy:
*   **Structure:** A Pytorch-based Neural Network.
    *   **Input Layer:** 10 nodes (the features).
    *   **Hidden Layers:** Two fully connected layers of 50 nodes each.
    *   **Activation:** ReLU (Rectified Linear Unit).
    *   **Output Layer:** 3 nodes (representing the Q-values for Long, Short, and No Position).
*   **Optimization:** Adam Optimizer.
*   **Experience Replay:** Stores past transitions and samples them randomly to "decorrelate" the data and stabilize training.

### 6. Execution Logic (The Strategy)
1.  **Calculate Spread:** The difference in price between Cointegrated Stock A and Stock B.
2.  **Generate State:** Feed the 10 features into the trained DQN.
3.  **Predict Action:** The DQN selects the action with the highest Q-value.
4.  **Mean Reversion:** If the spread is significantly above its mean (learned by the NN), the agent shorts the spread, betting it will contract. If significantly below, it longs the spread, betting it will expand back to the mean.
5.  **Exit:** The position is held until the DQN outputs a different action or a "No Position" signal.

### Summary of Results
The strategy proved highly effective on 2018 test data:
*   **Total Returns:** 131.33 across all 38 pairs.
*   **Top Performer:** The pair CTWS/AWR returned 71.28.
*   **Key Finding:** Increasing the "Negative Multiplier" decreases total returns but significantly increases the reliability and consistency of the trades the agent *does* choose to take.