# Cash-flow outcome comparison — authored reference

Case: `complete`. This is an illustration from the selected synthetic records, not an agent result or model-selection recommendation. Scope: DEMO-FLOWS, A r1 versus B r1, USD net flows, cutoff October 1, 2026 at 18:00 UTC.

F1–F3 have mature windows and supplied outcomes available by cutoff. F4 ends October 2 and is immature. It contributes no outcome error and is not treated as zero or as a mature missing observation. Forecasts must predate their target window; the model's name or a correct value cannot substitute for timing evidence.

Both models have eligible forecasts on F1–F3. A's absolute errors are USD0, USD0 and USD100,000; B's are USD10,000, USD10,000 and USD0. Mean absolute errors are approximately USD33,333.33 for A and USD6,666.67 for B, each with denominator three. The same IDs support the paired comparison: B minus A is approximately −USD26,666.67, an 80% relative reduction against A on this sample. The producer's lower-error claim is supported for these observations, not established as a general performance or economic advantage.

The selected case retains four expected cohort observations, three mature outcomes and one immature item. Both models have three paired eligible observations. These records establish neither an untouched holdout nor absence of training or selection overlap: that history is unavailable. There is no basis for statistical significance, deployment approval, calibrated probabilities, economic usefulness or company cost savings from this sample.

The three paired observations support the reported sample comparison. No model was trained, tuned, run or approved for this authored reference.

Locators: selected packet cohort F1–F4; forecasts A1–A4/B1–B4 as present, including issued/window fields; outcomes O1–O3 and available timestamps; producerClaim and trainingAndSelectionHistory; supplied comparison policy. Actual execution must retain its own result and artifact identities.
