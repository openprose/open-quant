# USD SOFR curve — interpolation decision

This is a methodology demonstration, not a complete regulatory submission. Institutional facts are supplied by the deploying institution.

## Purpose

The supplied model produces USD discount factors in a single-curve SOFR setting. This note covers its interpolation decision for the 2026-09-18 snapshot.

## Decision and reasons

The developer selected method B, the included Hagan–West monotone-convex forward-rate implementation, while retaining method A, log-linear discount-factor interpolation, as a comparison. The stated reason is forward-rate shape for projection. This is an attributed developer choice, not a universal preference or an institutional approval.

## Evidence and alternatives

The largest measured day-to-day overnight forward move through the last node was **59.71 bp for A and 1.68 bp for B**. Over five business days the respective maxima were **59.73 bp and 5.34 bp**. These observations support the stated forward-shape rationale within this snapshot; they do not prove smoothness at every point. Both methods closely reprice the selected input instruments.

## Limitations

B is less local in the supplied perturbation test. Increasing the 5Y quote by 1 bp changes forwards outside the 4Y–6Y window by up to **0.0305 bp under A and 4.1475 bp under B**. A may therefore be preferable when instrument-by-instrument hedge locality matters. This is one perturbation, not a test of every input. B also has flat stretches and short ramps, and its long-end behavior depends on sparse inputs and its end rule.

These results concern the model methods, not an advantage of OpenProse over another documentation approach. They do not establish production suitability.

## Institutional information

- [INSTITUTION-SUPPLIED: accountable model owner]
- [INSTITUTION-SUPPLIED: independent reviewer and actual review/approval status]
- [INSTITUTION-SUPPLIED: permitted production use and applicable implementation conventions]

## Source locators

The supplied brief records the choice and limitations. In [results.json](../inputs/results.json), `as_of` identifies the date; `forward_smoothness.A.max_jump_bp` and `.B.max_jump_bp` support the daily comparison; each method's `max_change_over_5_business_days_bp` supports the five-day comparison; `locality_bump_5Y_plus_1bp.A.max_change_outside_4Y_6Y_bp` and `.B.max_change_outside_4Y_6Y_bp` support the locality comparison; `repricing_max_abs_error_bp.A` and `.B` concern input repricing.
