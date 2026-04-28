Based on the AQR paper "A Century of Evidence on Trend-Following Investing," the strategy logic for their **Time Series Momentum (TSMOM)** approach can be extracted as follows:

### 1. Core Philosophy
The strategy is based on **Time Series Momentum**, which involves betting that an asset's recent trend will continue. Unlike "cross-sectional momentum" (ranking assets against each other), this strategy looks at each asset in isolation:
*   **Long:** If the asset’s past return was positive over the look-back period.
*   **Short:** If the asset’s past return was negative over the look-back period.

### 2. Investment Universe
The strategy is applied to **59 global markets** across four major asset classes:
*   **24 Commodities:** (e.g., Energies, Metals, Grains, Livestock).
*   **11 Equity Indices:** (e.g., S&P 500, FTSE 100, DAX, TOPIX).
*   **15 Bond Markets:** (e.g., US 10-year, Euro Bund, Long Gilt).
*   **9 Currency Pairs:** (G10 currencies vs. the US Dollar).

### 3. Signal Generation (Look-back Horizons)
The strategy does not rely on a single timeframe. Instead, it uses an **equal-weighted combination** of three look-back horizons to determine the trend:
*   **1-Month**
*   **3-Month**
*   **12-Month**

For each market, at the end of each month, the strategy calculates the return over these three periods. If the average signal is positive, the strategy goes long; if negative, it goes short.

### 4. Position Sizing and Risk Management
The strategy employs a two-tier risk-parity approach to ensure diversification and stable risk:

*   **Asset Level (Volatility Equalization):** Each individual position is sized to target the same amount of volatility. This prevents high-volatility assets (like Crude Oil) from dominating the risk of low-volatility assets (like 2-year Bonds).
*   **Portfolio Level (Volatility Targeting):** The aggregate portfolio of all 59 markets is scaled monthly to a constant **annualized ex-ante volatility target of 10%**.
*   **Covariance Estimation:** A simple covariance matrix is estimated using rolling 3-year equally weighted monthly returns to assist in the portfolio scaling process.

### 5. Implementation Details
*   **Instruments:** Uses liquid **futures contracts** where available. Prior to the existence of futures, it uses cash index returns financed at local short rates.
*   **Rebalancing:** The portfolio is rebalanced **monthly**.
*   **Transaction Costs:** Costs are deducted based on historical estimates. The paper assumes costs were significantly higher in the past (6x higher from 1903–1992 than they are today).
*   **Fees:** Returns are simulated net of a **2% management fee and 20% performance fee** (subject to a high-water mark).

### 6. Key Performance Logic (The "Why")
The paper argues that the strategy works because of:
*   **Investor Behavioral Biases:** Such as "anchoring" (reacting slowly to new information) and "herding" (buying what is already going up).
*   **Non-Profit Participants:** Central banks and corporate hedgers often trade for reasons other than profit (e.g., currency stabilization), which slows down the rate at which information is absorbed into prices, thereby creating trends.
*   **Convexity (The "Smile"):** The strategy exhibits a "smile" performance profile, meaning it tends to perform best during extreme equity bull markets or extreme bear markets (gradual declines allow the strategy to pivot to a short stance).

### Summary of Strategy Mechanics
| Component | Specification |
| :--- | :--- |
| **Signal Type** | Absolute (Time Series) Momentum |
| **Direction** | Long if $R_t > 0$, Short if $R_t < 0$ |
| **Look-backs** | 1-mo, 3-mo, 12-mo (equal-weighted) |
| **Asset Sizing** | Inverse volatility weighting (Equal Risk Contribution) |
| **Portfolio Risk** | Target 10% Annual Volatility |
| **Rebalance** | Monthly |
| **Asset Classes** | Equities, Fixed Income, Commodities, FX |