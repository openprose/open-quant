# Risk-report scope and house requirements

All positions, sensitivities, marks and scenario values are authored synthetic fixtures, not observed trading results or independently executed model outputs. The reader is the operating risk lead. Review TOY-RISK-BOOK r1 under TOY-VALUATION r1, using USD clean values for positions P1 and P2. No other institution-specific facts or approvals are supplied or required for this reporting obligation.

## Daily movement

The interval is September 29 to September 30, 2026, at 20:00 UTC. The reporting total is closing minus opening value of the fixed two-position book, with no trades, cash flows, fees or other adjustments. This is the example's mark-to-market movement, not an accounting posting or a regulatory P&L attribution test.

The required explanation consists of rates, spreads and carry, for each position. Rates and spreads are first-order approximations: multiply each opening sensitivity in USD per basis point by its supplied daily basis-point move. Carry amounts are supplied separately. Keep the residual as total movement minus supported explanatory components. The absolute portfolio residual must be no more than USD1,000 to meet this illustrative explanation tolerance; equality passes. Also report position-level residuals, without inventing position-level limits. Netting can hide large offsetting residuals; retain them.

Both factor sensitivities for each position, both daily moves and both carry observations are required. A missing component leaves the complete explanation and residual unresolved; a partial-component subtotal must be identified as partial. Never fill a gap with zero or assign the residual to an invented driver. Consistent arithmetic does not validate the source sensitivities, factor labels or economic explanation.

## Scenarios and sensitivities

The expected scenarios are rates (+100 bp parallel rate move), spreads (+100 bp spread move), and joint (both moves together). All use the September 30 closing marks as base, the same fixed book, USD clean values, model/portfolio r1 and an instantaneous horizon. One basis point is an absolute 0.01 percentage-point rate change. Values are supplied full scenario snapshots, not estimates obtained by scaling the opening daily sensitivities. Other inputs are held fixed by the fixture's assumptions; no scenario probabilities are supplied.

Each scenario requires one value for each position. Compare complete scenario values with the compatible closing base. The permitted unmitigated loss is at most USD25,000 per scenario; equality passes. Missing or duplicate positions, mismatched identity/basis/currency, a different base time, or an incompatible horizon leave that scenario's full-book finding unresolved. Report known subsets separately. A known breach in another complete scenario still prevents an overall all-clear.

Report the sum of single-factor effects and the supplied joint effect, with their difference. Different scenarios are alternatives, not additive realized losses. H1's figures are hypothetical incremental hedge P&L. Show the arithmetic after that assumption separately; it does not replace unmitigated-limit assessment or prove approval, execution, cost or feasibility. No order, trade or accounting action is authorized.

The reporting obligation is to explain these findings and evidence limitations. It can be fulfilled when a numerical limit is breached or evidence is missing. Producer statements do not override observations or the selected requirements.
