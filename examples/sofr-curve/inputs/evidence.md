# Reading the retained numerical evidence

[results.json](results.json) is an unchanged OpenProse calculation record from the predecessor example. [Provenance](../../../provenance/README.md) identifies the source revision and imported hashes. These are historical observations, not current market data or a new model run.

The common as-of date is the `as_of` field. A denotes log-linear discount factors; B denotes the included Hagan–West monotone-convex implementation. Relevant field locators:

| Meaning | JSON field | Unit and scope |
|---|---|---|
| Largest absolute input repricing error | `repricing_max_abs_error_bp.A` and `.B` | bp; selected input instruments |
| Largest day-to-day overnight forward move | `forward_smoothness.A.max_jump_bp` and `.B.max_jump_bp` | bp; measured grid through the last node |
| Largest five-business-day forward move | `forward_smoothness.A.max_change_over_5_business_days_bp` and `.B.max_change_over_5_business_days_bp` | bp; measured grid through the last node |
| Response away from a perturbed quote | `locality_bump_5Y_plus_1bp.A.max_change_outside_4Y_6Y_bp` and `.B.max_change_outside_4Y_6Y_bp` | bp; +1 bp to 5Y, outside the 4Y–6Y window |
| Largest absolute discount-factor difference | `df_difference_A_minus_B_monthly_grid.max_abs` | discount factor; monthly grid; date in `max_abs_date` |
| Same difference for a USD100 million payment | `df_difference_A_minus_B_monthly_grid.max_abs_pv_per_notional_usd` | USD; one payment on that worst-difference date |

These observations do not establish financial suitability, institutional approval or superior documentation performance. A claim about continuity at every possible point needs more than a finite-grid maximum. The brief's preference is attributed to its developer, not inferred solely from these numbers.

The separate quotes and fixing inputs support optional numerical reproduction; they are not additional house requirements. Public market data inputs were drawn from DTCC public price dissemination and New York Fed SOFR records. Raw transaction archives and third-party papers are not distributed here. See [source notices](../../../provenance/README.md#external-sources).
