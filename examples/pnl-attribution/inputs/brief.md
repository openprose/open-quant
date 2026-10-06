# Synthetic P&L attribution scope

Review the movement of a fixed long position in 10,000 European calls, strike 100, under one unchanged Black valuation formula. Forward changes 100→110, annual volatility 0.20→0.30 and remaining maturity 1→0.75 years; continuous discount rate stays 0.03. Values are USD for the whole position. There are no trades, fees, cash flows, exercise or quantity changes.

The eight corners form a counterfactual valuation grid, not an observed temporal sequence. Bit order is forward, volatility, maturity; zero chooses the original endpoint and one the new endpoint. At every corner, discount is exp(−0.03T) and standard deviation is σ√T. Forward is supplied independently; the maturity change does not derive a different forward from spot or carry. The maturity label therefore describes this specific joint change in remaining time, discount and standard deviation.

`corners` contains native outcomes and separate elementary-formula references. `reported_attribution` contains the producer's downstream calculations. A downstream value may imply a missing corner number without independently establishing the actual native valuation. Preserve that distinction, including a retained producer success flag when its numerical record is unavailable.

This is a model-based mark-to-market bridge over supplied endpoints. It does not establish actual market causality, an accounting result, the regulatory P&L attribution test, institutional acceptance or savings.
