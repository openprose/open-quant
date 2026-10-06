# Cash-flow outcome comparison — authored reference

This is an illustration from synthetic records, not an agent result or model-selection recommendation. Scope: DEMO-FLOWS, A r1 versus B r1, USD net flows, cutoff October 1, 2026 at 18:00 UTC.

F1–F3 have mature windows and supplied outcomes available by cutoff. F4 ends October 2 and is immature. It contributes no outcome error and is not treated as zero or as a mature missing observation. Forecasts must predate their target window; the model's name or a correct value cannot substitute for timing evidence.

**Complete.** Both models have eligible forecasts on F1–F3. A's absolute errors are USD0, USD0 and USD100,000; B's are USD10,000, USD10,000 and USD0. Mean absolute errors are approximately USD33,333.33 for A and USD6,666.67 for B, each with denominator three. The same IDs support the paired comparison: B minus A is approximately −USD26,666.67, an 80% relative reduction against A on this sample. The producer's lower-error claim is supported for these observations, not established as a general performance or economic advantage.

**Missing.** B3 is absent. A's three-observation descriptive mean remains USD33,333.33; B's two-observation descriptive mean is USD10,000. Comparing those unequal populations would favor B while omitting the observation on which A has its largest error. The common population is F1/F2: A's mean is zero and B's USD10,000, so B minus A is +USD10,000. A has lower error on this two-item subset. A relative reduction against A is undefined because its mean error is zero. Neither this result nor an invented B3 establishes a full three-item comparison. The producer's blanket claim is unsupported by a comparable full-cohort result.

**Late forecast.** B3 is issued September 30 at 17:06 UTC, after F3's 09:00–17:00 window and the 17:05 outcome availability. Its matching USD100,000 value is not eligible predictive evidence. Coverage and metrics therefore match the two-item comparison above, but the reason is timing incompatibility rather than an absent record. Preserve that distinction.

All cases retain four expected cohort observations, three mature outcomes and one immature item. Complete has three paired eligible observations; missing and late-forecast have two. These records establish neither an untouched holdout nor absence of training or selection overlap: that history is unavailable. There is no basis for statistical significance, deployment approval, calibrated probabilities, economic usefulness or company cost savings from this sample.

Accurate reporting may be fulfilled despite incomplete paired coverage. Obtain the actual admissible missing forecast or report its absence; do not backdate a forecast or borrow another case's value. No model was trained, tuned, run or approved.

Locators: selected packet cohort F1–F4; forecasts A1–A4/B1–B4 as present, including issued/window fields; outcomes O1–O3 and available timestamps; producerClaim and trainingAndSelectionHistory; supplied comparison policy. Actual execution must retain its own result and artifact identities.
