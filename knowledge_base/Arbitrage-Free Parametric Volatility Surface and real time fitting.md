Based on the provided presentation slides by Timothy Klassen, the strategy logic for designing and fitting arbitrage-free volatility surfaces can be broken down into four core pillars: **Dividend Modeling**, **Volatility Curve Parametrization**, **No-Arbitrage Constraints**, and **Fitting Methodology**.

---

### 1. Dividend Modeling: The Hybrid Model
The strategy rejects the standard "Spot Model" (where dividends simply drop the stock price) in favor of a **Hybrid Model**.
*   **Logic:** Treat the stock price as $S_t = \tilde{S}_t + D_t$, where $D_t$ is the present value of future dividends and $\tilde{S}_t$ (the "pure" stock) follows Geometric Brownian Motion (GBM).
*   **Blending Scheme:** Use a transition from **Cash Dividends** in the short term to **Discrete Proportional Dividends** in the long term. This provides a "cash buffer" that makes modeling local volatilities and Greeks more stable.
*   **Purpose:** This allows for "De-Americanization" of option prices into European equivalents, which is necessary for clean surface fitting.

### 2. Volatility Curve Parametrization
The strategy utilizes a parametric approach rather than non-parametric splines to ensure stability and parsimony.
*   **Normalized Strike ($z$):** Instead of using raw strike $K$, use a normalized log-moneyness:
    $$z = \frac{\log(K/F)}{\sigma_0 \sqrt{T}}$$
    *(Where $\sigma_0$ is the At-the-Forward (ATF) volatility).*
*   **The Shape Function ($f(z)$):** The total variance is defined by a shape curve:
    $$\sigma(z)^2 = \sigma_0^2 f(z|p)$$
*   **Key Parameters:**
    *   **$s_2$ (Skew):** The slope of the shape curve at the money.
    *   **$c_2$ (Convexity/Smile):** The curvature of the shape curve.
    *   Expansion: $f(z) \approx 1 + s_2 z + \frac{1}{2} c_2 z^2$

### 3. No-Arbitrage Logic
The core of the strategy is enforcing mathematical constraints to ensure the surface is tradable and consistent.

#### A. Static (Butterfly) Arbitrage
The implied probability density $\rho$ must be non-negative. This is checked using the Durrleman condition/Klassen formulation $g(y) \ge 0$.
*   **ATF Constraint:** At the center of the curve ($z=0$), the skew is mathematically capped by the convexity:
    $$s_2^2 \le \frac{4 + 2c_2}{1 + \frac{1}{4} \hat{\sigma}_0^2}$$
*   **Implication:** If the market skew is too steep for the given smile curvature, butterfly arbitrage exists.

#### B. Calendar Arbitrage
The total Black-Scholes variance $w(y) = T\sigma(y)^2$ must be non-decreasing in time ($T$) for a fixed log-moneyness ($y$).
*   If $w(y, T_2) < w(y, T_1)$ for $T_2 > T_1$, a calendar spread arbitrage exists.

#### C. Asymptotic Constraints
To prevent "moments exploding," the total variance must satisfy the Lee Moment Formula as $y \to \infty$:
$$w(y) \le 2|y|$$

### 4. Fitting Methodology in Practice
*   **Term-by-Term Fitting:** Fit individual curves for each expiry one at a time, but impose a "smoothness" penalty or constraint across the term structure.
*   **Factorization:** Factor out the overall volatility level ($\sigma_0$) first, then solve for the shape parameters ($s_2, c_2$).
*   **Stability:** Parameters should be "independent" and stable day-over-day. The strategy aims to fit standard models (like SLVJ) within a few basis points without "hacks" in the wings.

### Summary of Strategy Flow
1.  **Clean the Data:** Convert American option prices to European equivalents using the Hybrid Dividend Model.
2.  **Normalize:** Map strikes to $z$-space using ATF volatility.
3.  **Parametrize:** Define the curve using $s_2$ (slope) and $c_2$ (curvature).
4.  **Constrain:** Apply the $g(z) \ge 0$ inequality to ensure no butterfly arbitrage and ensure total variance increases with time.
5.  **Calibrate:** Minimize the distance between the parametric curve and market mid-prices while maintaining the no-arbitrage boundaries.