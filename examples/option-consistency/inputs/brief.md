# Two synthetic European call slices

Review one constant-20%-standard-deviation slice and one authored-price slice. Both calculations use forward 100, unit discount, one-year maturity, zero displacement and strikes 80, 90, 105, 110 and 130. Prices are USD per unit-notional option. The cases are synthetic single-expiry slices, not a volatility surface or actual market data.

`calculation_assumptions` describes what the calculation assumed. `selected_instrument_terms` supplies the caller's synthetic stipulations about the instruments being reviewed. A missing selected term remains unknown even if the calculation or a producer assertion assumes it. The same strike schedule applies to both slices; changing the slice changes quotes, not the stipulated instrument identity.

Native inversion outcomes, repriced calls/puts, independent roots, exact strategy weights, payoff nodes, tail slopes and purchase costs are retained. Puts were constructed by parity; they are not independent observed put quotes. QuantLib standard deviation is annual volatility multiplied by the square root of maturity. At one year their numerical values coincide, without making the quantities interchangeable.

The report reviews this finite scope. It does not certify an entire surface, authorize trading, establish institutional acceptance or estimate operating savings.
