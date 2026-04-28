Based on the paper provided, here is the extracted strategy logic for the Deep Reinforcement Learning (DRL) stock trading approach.

---

### 1. Mathematical Framework: Markov Decision Process (MDP)
The strategy treats the stock market as an interactive environment, modeled as an MDP with the following components:

*   **State Space ($s = [p, h, b]$):**
    *   **$p$ (Prices):** A vector of the current market prices for the 30 stocks ($p \in \mathbb{R}^{30}_+$).
    *   **$h$ (Holdings):** A vector of the number of shares currently held for each stock ($h \in \mathbb{Z}^{30}_+$).
    *   **$b$ (Balance):** The remaining liquid cash available in the portfolio ($b \in \mathbb{R}_+$).
*   **Action Space ($a$):**
    *   A vector representing the actions for all 30 stocks. 
    *   For each stock: **Sell** (decrease holdings), **Buy** (increase holdings), or **Hold** (no change).
*   **Reward Function ($r$):**
    *   The reward is defined as the change in the total **Portfolio Value** after taking an action.
    *   **Portfolio Value** = (Sum of equities in held stocks $p^Th$) + (Balance $b$).
    *   The goal is to maximize the cumulative reward $\sum r_t$, which is equivalent to maximizing the final portfolio value.

### 2. Core Algorithm: Deep Deterministic Policy Gradient (DDPG)
Because the action space in stock trading is large (30 stocks with various quantities), the authors use DDPG, which is an **Actor-Critic** framework designed for continuous and high-dimensional action spaces.

*   **The Actor Network ($\mu$):** Learns the optimal policy by mapping states directly to actions. It decides how many shares of which stock to buy or sell.
*   **The Critic Network ($Q$):** Evaluates the action taken by the actor by estimating the Q-value (expected future return).
*   **Experience Replay:** The agent stores past transitions $(s_t, a_t, r_t, s_{t+1})$ in a buffer. It samples these randomly during training to break the correlation between consecutive trading days.
*   **Target Networks:** The strategy uses "target" versions of the Actor and Critic networks that update slowly (using a parameter $\tau$). This provides stability and prevents the model from diverging during training.

### 3. Execution Logic and Constraints
The strategy follows specific rules to ensure the trading is realistic:

*   **Sequential Execution:** To maintain a positive balance, the strategy assumes selling orders are executed first to increase the balance, followed by buying orders.
*   **Budget Constraint:** The total cost of bought stocks cannot exceed the current balance plus the proceeds from stocks sold in that same time step.
*   **Exploration:** During training, a random noise process ($\mathcal{N}$) is added to the actor's output to encourage the agent to explore different trading maneuvers rather than sticking to a single known path too early.

### 4. Training and Adaptation Strategy
The paper employs a specific data-split and continuous learning logic:

1.  **Stage 1: Training (2009–2014):** The agent learns basic market patterns and price movements.
2.  **Stage 2: Validation (2015–2016):** Used to tune hyperparameters like learning rate and the number of training episodes.
3.  **Stage 3: Trading with Adaptive Learning (2016–2018):** 
    *   This is a "Live" test phase.
    *   **Key Logic:** The agent **continues to train** while it is trading. By incorporating new daily data as it arrives, the agent adapts its strategy to changing market dynamics (Incremental Learning).

### 5. Performance Benchmarks
The strategy’s success is measured against two traditional baselines:
*   **Dow Jones Industrial Average (DJIA):** A passive "Buy and Hold" strategy of the index.
*   **Min-Variance Portfolio Allocation:** A traditional Markowitz-based approach that seeks to minimize risk for a given return.

**Resulting Advantage:** The DDPG logic achieved an annualized return of **25.87%**, significantly higher than the DJIA (16.40%) and Min-Variance (15.93%), with a superior Sharpe Ratio (1.79), indicating better risk-adjusted returns.