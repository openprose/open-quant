# SOFR change comparison — authored reference for both modes

This is a hand-authored illustration of two separate agreements, not the output of either command. It reuses the historical September 18, 2026 calculation record for synthetic request SOFR-CHANGE-EXAMPLE-1: compare hypothetical current method A with proposed method B.

| Measure | A | B | Selected limit |
|---|---:|---:|---|
| Maximum repricing error, bp | 3.8601 × 10⁻⁹ | 2.7554 × 10⁻¹⁰ | At most 0.000001 in both modes. |
| Maximum daily forward move, bp | 59.7120 | 1.6846 | At most 2 in both modes. |
| Maximum off-window response, bp | 0.03046 | 4.14753 | At most 1 only in shape-and-locality. |

Source: `examples/sofr-curve/inputs/results.json`, `repricing_max_abs_error_bp`, `forward_smoothness.*.max_jump_bp`, and `locality_bump_5Y_plus_1bp.*.max_change_outside_4Y_6Y_bp`. Figures are rounded for display; comparisons use the retained values. Requirements: `house/shape.md` and, where selected, `house/locality.md`.

In **shape**, both methods meet the repricing limit; A breaches the daily-move limit and B meets it. The proposed B configuration therefore meets this selected numerical set. Its larger off-window response remains a material disclosed tradeoff, but the unselected locality limit is not a reason to fail this agreement's numerical finding.

In **shape-and-locality**, B breaches the additional locality limit. A meets that limit but still breaches the daily-move limit. Neither method meets all three selected criteria. B's shape benefit does not waive the locality requirement. Recommending a different limit would propose a changed agreement.

The comparison supports only the supplied snapshot and measures. Repricing errors concern solver tolerance, not model risk; the grid does not prove universal smoothness. The locality test is one +1 bp perturbation at 5Y, measured outside 4Y–6Y. The brief also records flat stretches, short ramps and sparse long-end inputs. No new model calculation, production migration, current market assessment or institutional approval is established.

Either reporting invocation can be fulfilled by making its corresponding finding accurately. This authored reference provides no execution evidence for either invocation.
