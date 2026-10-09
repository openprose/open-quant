# USD SOFR curve: interpolation decision

This is a methodology demonstration, not a complete regulatory submission. Institutional facts are supplied by the deploying institution.

## Purpose

The model produces discount factors for USD cash flows in a single-curve SOFR setting for the 2026-09-18 as-of date. This bounded decision concerns interpolation; it does not cover other currencies, multi-curve construction, production deployment, or institutional approval. [Brief, scope](../../../examples/sofr-curve/inputs/brief.md)

## Decision and reasons

Method A is log-linear interpolation of discount factors, implemented with QuantLib. Method B is the unameliorated Hagan–West monotone-convex forward-rate method, including its positivity collar; it is not QuantLib’s default smoothed ConvexMonotone variant. The supplied developer brief chooses **method B**, while retaining method A as the comparison. The developer’s stated reason is the shape of projected forward rates, not a claim that B is universally preferable. [Brief, methods and choice](../../../examples/sofr-curve/inputs/brief.md)

## Evidence and alternatives

Both methods closely reprice the selected input instruments: the maximum absolute errors are 3.860106679e-09 bp for A and 2.755434769e-10 bp for B (`repricing_max_abs_error_bp.A` and `.B`). On the measured grid through the last node, B’s largest day-to-day overnight-forward move is 1.684593955 bp versus A’s 59.71204085 bp (`forward_smoothness.B.max_jump_bp` and `.A.max_jump_bp`). This finite-grid result is the supplied benefit supporting the developer’s choice; it is not proof of smoothness everywhere. Both methods are viable alternatives for this snapshot. [Results and field meanings](../../../examples/sofr-curve/inputs/evidence.md)

## Limitations

The material trade-off is locality. For a +1 bp 5Y-quote perturbation, the largest forward change outside the 4Y–6Y window is 4.147533778 bp for B versus 0.030463316 bp for A (`locality_bump_5Y_plus_1bp.B.max_change_outside_4Y_6Y_bp` and `.A.max_change_outside_4Y_6Y_bp`). This is one selected perturbation, not a norm over every input; A may therefore be preferable for instrument-by-instrument hedging. The results are historical observations for 2026-09-18, not a new run or current market data. [Brief and evidence guide](../../../examples/sofr-curve/inputs/brief.md); [results fields](../../../examples/sofr-curve/inputs/evidence.md)

## Institutional information

- [INSTITUTION-SUPPLIED: accountable model owner]
- [INSTITUTION-SUPPLIED: independent reviewer and actual review/approval status]
- [INSTITUTION-SUPPLIED: permitted production use and applicable implementation conventions]

No institutional approval, certification, or completed model review is established by this note. [Institutional-facts input](../../../examples/sofr-curve/inputs/institutional-facts.md)

## Source-locator list

- `examples/sofr-curve/inputs/brief.md`: developer choice, rationale, scope, and limitations.
- `examples/sofr-curve/inputs/evidence.md`: permitted result fields, units, scope, and as-of-date convention.
- `examples/sofr-curve/inputs/results.json`: `as_of`; `repricing_max_abs_error_bp`; `forward_smoothness`; `locality_bump_5Y_plus_1bp`.
- `examples/sofr-curve/inputs/institutional-facts.md`: unresolved institutional slots.
