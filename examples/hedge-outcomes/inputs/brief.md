# Hypothetical hedge comparison

Subject: TOY-HEDGE r1, one synthetic position and one hedge instrument. Two periods each contain four observations. All dates, selection records and positions are authored examples; the receipt establishes a numerical calculation, not historical trading or decision records. There are no actual trades, costs, funding, fees, margin or institutional approvals.

The position's P&L `y` is in thousands of USD. Hedge P&L `x` is in thousands of USD per standard lot. Selecting `h` standard lots contributes `-h*x`, so total hypothetical P&L is `y-h*x`. Equivalently, `h*x` is the fitted component of the position P&L and `y-h*x` its residual. No intercept is fitted. The same four observations must support each within-period comparison. Training and later observations are separate; hypothetical earlier selection does not establish real prospective forecasting performance.

Native fits minimize the sum of squared residuals (SSE). S1 fits the training period, S2 the later period and S3 the training period with hedge P&L expressed per 100-lot basket. S4 and S5 fit training under bounds of ±1 standard lot and ±0.01 baskets respectively. A basket contains 100 standard lots: scaling `x` by 100 requires dividing an equivalent position coefficient by 100. The selected original position limit applies in standard lots to every candidate, including unconstrained fits.

Native NumPy outputs include squared residual sums, matrix rank and singular values, but no Boolean success field. SciPy's native cost is half the SSE and its residual vector is `Ax-y`; reported total P&L is `y-Ax`. Their signs differ without changing SSE. A returned fit is not an acceptance decision.

The packet supplies quadratic coefficients `[a,b,c]` for `a*h²+b*h+c` in standard lots. Positive curvature can establish an unconstrained global minimum; a bounded minimum must also respect the original interval. These are algebraic comparison references, not uncertainty estimates.

All observed vectors have mean zero in this construction. Population variance uses denominator four and equals SSE/4 here. Relative SSE reduction is `1 - candidate SSE / unhedged SSE` for the same period. It is not a cash saving or a general equality between squared error and variance. Correlation is dimensionless; identical correlation after scaling does not establish equivalent position units or correctly converted limits.
