# Synthetic backtest population

Model: `TOY-VAR`, revision `r1`. Portfolio: `DEMO-BOOK`, unchanged across the supplied observations. Owner: the synthetic Market Risk team. All observations and policies are authored examples, not actual risk results.

Expected dates: September 21, 22, 23, 24 and 25, 2026. Each date has one USD VaR forecast at a stated 99% confidence level and two separately defined outcomes, actual P&L (APL) and hypothetical P&L (HPL). Horizon: the synthetic one-day window from 09:00 to 17:00 UTC on that date. Forecast timestamps must precede 09:00 UTC. No claim is made about how these toy forecasts were estimated or calibrated.

APL represents the supplied actual daily P&L; HPL represents the supplied daily P&L on a fixed opening portfolio. Their numerical values are supplied, not reconstructed here. No further decomposition, fees or valuation adjustments are available. The house policy governs the scope of this illustration, not institutional implementation of either definition.
