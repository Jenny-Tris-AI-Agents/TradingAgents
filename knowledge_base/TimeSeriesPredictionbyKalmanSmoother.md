The strategy logic described in the paper follows a multi-stage approach using **Optimal Linear Filtering** and **Smoothing**. The core innovation is the decomposition of the time series into a long-term trend and a short-term periodic component, both estimated via the Kalman Smoother.

Below is the extracted strategy logic:

### 1. General Architecture
The prediction is additive. The final signal estimate $\hat{y}_k$ is the sum of two distinct models:
$$\hat{y}_k = \hat{x}_k (\text{Long Term}) + \hat{d}_k (\text{Short Term})$$

---

### 2. Long-Term Model (Trend Logic)
The authors assume the underlying signal is locally linear with a derivative that behaves like a Brownian noise process.
*   **State Space:** The state $x_k$ includes the position and the first derivative (velocity).
*   **Dynamics:** A continuous-time model discretized for varying sampling rates. This allows for prediction over missing data points.
*   **Process Noise:** Applied to the second derivative (white noise model), which results in a smooth curve that adapts to "sudden changes in derivatives" (turning points).
*   **Implementation:**
    1.  **Kalman Filter:** Run over the sequence to estimate means and covariances.
    2.  **Kalman Smoother:** Run backward over the filter results to produce the MAP (Maximum A Posteriori) estimate for both known and missing data.

---

### 3. Short-Term Model (Residual/Periodicity Logic)
After subtracting the long-term trend, the residuals exhibit periodicity. This is handled by a **Time-Varying Autoregressive (AR) Model**.
*   **Varying Weights:** Unlike standard AR models, the weights $w_k$ are allowed to evolve over time according to a Gaussian random walk: $w_k = w_{k-1} + \text{noise}$.
*   **Order:** A second-order AR model was selected (using two weights).
*   **Logic:** This accounts for non-stationarity in the local cycles of the time series.

---

### 4. Parameter Selection via Cross-Validation
To prevent overfitting (especially given the high number of effective parameters in a time-varying AR model), the authors do not use Maximum Likelihood.
*   **Measurement Noise ($\sigma^2$):** Determined via visual inspection of residuals.
    *   Long-term: $\sigma^2_x = 10^2$
    *   AR estimation: $\sigma^2_{ar} = 12$
    *   Final periodicity: $\sigma^2_p = 10^{-9}$ (set very low to force the model to follow measurements exactly when they exist).
*   **Process Noise ($q$):** This is the "tuning knob." The spectral densities for the trend ($q_x$) and the AR weights ($q_{ar}$) are selected by **Cross-Validation** to minimize the target error criterion.

---

### 5. Execution Workflow (The 6-Step Process)
The strategy is executed in a sequential pipeline:

**Part A: Long Term**
1.  **Filter/Smooth Trend:** Apply Kalman Smoother to the raw data using the locally linear model to extract $\hat{x}_k$.
2.  **Calculate Residuals:** $e_k = y_k - \hat{x}_k$.

**Part B: Short Term**
3.  **Estimate AR Weights:** Run a Kalman Filter/Smoother on the residuals $e_k$ to determine how the AR coefficients $w_k$ change over time.
4.  **Predict Weights:** Project these weights into the missing data intervals.
5.  **Estimate Periodicity:** Using the smoothed weights, run a Kalman Filter/Smoother on the residuals to extract the periodic component $\hat{d}_k$.
6.  **Synthesize:** Add the smoothed trend $\hat{x}_k$ and the smoothed periodicity $\hat{d}_k$ to get the final prediction.

---

### 6. Key Strategy Insights
*   **Smoothing vs. Filtering:** The "Smoother" is critical because it uses future data to refine past estimates, making it superior to a standard Filter for filling gaps in a historical time series (interpolation).
*   **Information Decay:** The model logic acknowledges that as you move further from a known measurement into a missing interval, the "phase" information of the local periodicity becomes less certain. Therefore, the short-term model naturally decays toward the long-term mean in the middle of large gaps.
*   **Linearity:** Despite the time series being non-linear, the authors demonstrate that a combination of two linear state-space models (one for trend, one for time-varying AR) can effectively approximate complex non-linear behavior.