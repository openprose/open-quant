# USD SOFR discount-curve methodology

This is a public methodology demonstration, not a complete regulatory submission. Institutional facts are supplied by the deploying institution.

**Authored reference for the complete supplied-evidence case.** This document was not produced by an agent invocation of the accompanying program.

## Purpose and scope

The model constructs discount factors for USD cash flows in a single-curve SOFR setting as of September 18, 2026. The retained spot date is September 22. Method A uses QuantLib's log-linear interpolation of discount factors. Method B uses the included unameliorated Hagan–West monotone-convex forward interpolator with a positivity collar. The supplied developer selected B for forward-shape behavior and retained A as a comparison. This account does not establish actual deployment, other-currency use, multi-curve suitability or institutional acceptance. [Sources: brief.md; results.json: as_of, spot; bootstrap.py: CurveSet.]

## Inputs and provenance

The calculation uses the committed derived quotes and SOFR fixing. Quotes are stored in percent and converted to decimal rates; only rows with used_in_bootstrap=True enter the build. Twenty OIS tenors are used, from 1M through 30Y, with 9M and 25Y excluded. Two short deposits bring the calibration set to 22 instruments. The fixing input is 3.85%, identified as the last known September 17 fixing. Later realized-fixing fields in the JSON are not used by load_inputs. [Sources: quotes.csv; sofr-fixing.json; results.json: instruments; bootstrap.py: load_inputs, ql_helpers.]

The input files include trade-count and dispersion indicators, but they do not reproduce raw trade filtering or quote estimation. The supplied provenance identifies DTCC public dissemination and New York Fed records as upstream sources. This account is conditional on the retained derived inputs; it does not certify their acquisition, timeliness for a production feed or economic representativeness. Source identities and external-use notices remain in the register. [Sources: provenance/import.json; provenance/README.md; quotes.csv.]

## Construction and conventions

Curve time uses Act/365 Fixed. Deposit and coupon accruals use Act/360. QuantLib's SOFR calendar constructs dates; swaps start two business days after as-of, use annual fixed-leg payments, Following adjustment and a two-business-day payment lag. Both overnight and tom-next deposits use the same supplied fixing. These are observed implementation conventions, not an institution's approved settings. [Source: bootstrap.py: constants, ql_helpers, hw_instruments.]

A builds PiecewiseLogLinearDiscount from the selected helpers. B receives those same instrument dates but prices through its own discount curve. Its OIS par rate is the sum of discounted period floating cash flows divided by the fixed-leg annuity. A floating period uses the start/end discount-factor ratio minus one, discounted to its payment date. This is the implemented single-curve calculation. [Sources: bootstrap.py: CurveSet, hw_instruments; hagan_west.py: Ois, ois_par_rate.]

B solves for interval discrete forwards simultaneously because neighboring intervals affect interpolation. Deposit forwards are derived from their simple-interest relation. The interpolator estimates node forwards from adjacent intervals, applies its configured collar, and selects piecewise functions from endpoint deviations. It integrates those forwards to obtain discount factors as exp(-integral). The implementation uses SciPy's hybrid root solver with requested tolerance 1e-14, then rejects a maximum par-rate residual above 1e-11. Those numerical settings do not establish economic accuracy. [Source: hagan_west.py: MonotoneConvex, _sector, _g, _G, bootstrap.]

## Developer choice and observed comparisons

The developer's reason for choosing B is its forward-rate shape on this snapshot, not a universal ranking. The main tradeoff is weaker locality under the selected quote perturbation. Both alternatives closely fit the same instruments. [Source: brief.md.]

| Measure | A | B | Scope |
|---|---:|---:|---|
| Maximum absolute repricing error, bp | 3.86011e-9 | 2.75543e-10 | 22 selected instruments |
| Largest daily forward move, bp | 59.712041 | 1.684594 | Business-day grid through the last node |
| Largest five-business-day move, bp | 59.727047 | 5.338172 | Same bounded comparison |
| Largest outside-window response, bp | 0.030463 | 4.147534 | +1 bp to 5Y, outside actual 4Y–6Y pillars |

The inside locality interval is September 25, 2030 through September 24, 2032, including endpoints; outside excludes those dates. It is not a nominal 4.0-to-6.0-year interval. The last node is September 26, 2056. Daily and five-day measures are different; neither proves global smoothness or stability under arbitrary inputs. A's smaller observed outside-window response can matter for local sensitivities, while the single bump does not characterize every perturbation. [Sources: results.json: repricing_max_abs_error_bp, forward_smoothness, locality_bump_5Y_plus_1bp; bootstrap.py: days, d4, d6; brief.md.]

## Variants, conventions and endpoint behavior

B holds its instantaneous forward constant beyond the last node. The observed overnight forward there and one year later is about 3.995695%. This end rule and sparse long-end inputs limit extrapolation conclusions. [Sources: hagan_west.py: forward, integral; results.json: forward_smoothness.B.]

The no-collar variant converged and made no recorded monthly-grid difference in this snapshot; no collar nodes were binding. That does not establish that the option is irrelevant for other inputs. QuantLib's default ConvexMonotone settings (0.3, 0.7) converged as a different variant, with a largest daily forward move of about 20.556157 bp. The attempted (0, 1) setting failed its iterative bootstrap. A similar method name therefore does not identify the same implementation. [Source: results.json: interpolation_variants, hagan_west_collar_binding_nodes.]

Changing the payment lag from two business days to zero changed B's monthly-grid discount factors by up to 4.791807e-6, equivalent to about USD479.18 for the stated USD100 million single payment at that variant's worst-difference grid point. This is a conditional convention comparison, not approval of either setting. [Sources: results.json: convention_sensitivities.payment_lag_0_vs_2.B; bootstrap.py: NOTIONAL, convention comparisons.]

## Present-value interpretation

The largest absolute A/B discount-factor difference on the monthly grid is 0.002274582, on April 18, 2050. Applied to a single USD100 million payment on that date, it is about USD227,458.20. This is a valuation difference between interpolation methods under fixed inputs, not trading profit, portfolio savings or a benefit caused by documentation software. [Sources: results.json: df_difference_A_minus_B_monthly_grid; brief.md.]

## Limitations and unresolved institutional facts

These observations concern one as-of date, selected inputs, finite grids and specific perturbations. B can have flat stretches and short ramps; the five-day result prevents treating its smaller daily maximum as uniformly small movement at every horizon. Calibration fit is not evidence of prediction, market suitability or complete implementation coverage. The source describes assumptions and numerical choices; several economic rationales are not supplied and remain explicit in the choice register. [Sources: brief.md; results.json; reviews.md: Choice register.]

The October 6 reproduction receipt records a successful comparison using the same derived inputs and identified source, with relative tolerance 1e-10 and absolute tolerance 1e-12. It did not repeat raw acquisition or quote derivation. This reference document has not itself run a model, established an independent institutional review or examined production controls. [Source: provenance/reproduction/2026-10-06.json.]

- [INSTITUTION-SUPPLIED: accountable model owner]
- [INSTITUTION-SUPPLIED: independent reviewer and actual review/approval status]
- [INSTITUTION-SUPPLIED: permitted production use and applicable implementation conventions]

These are absent supplied facts, not evidence that approval or deployment never occurred. No production monitoring policy or threshold is invented. Disclosure satisfies the selected public-document requirement; institutional completion remains separate. [Source: institutional-facts.md; requirements.md: D9.]

## Source-locator convention

Brief, quotes, fixing, institutional facts and numerical locators refer to the files bound by [the source register](../inputs/sources.md). Code locators identify functions or variables in its two registered model files. Provenance locators refer to the registered repository records. These are source-inspection and observation claims, not assertions about unprovided paper contents.
