# Pricing probabilities and intended use

Public reproduction plan, prespecified October 6, 2026. This is an elementary synthetic construction, not new pricing theory, financial advice or an empirical forecast. It tests an important reporting distinction with existing contracts.

## Question and fixed construction

Can complete and correctly reproduced prices identify the real-world probabilities needed for a different intended use?

One period, dates t=0 and T=1 year, USD, no dividends, taxes, transaction costs or default. The only terminal stock states are down=80 and up=130. A bond paying USD1 in either state costs 20/21 at t=0; one share costs USD100. Short positions and arbitrary real holdings are permitted in this mathematical market. These are stipulated assumptions, not observations about a traded stock.

Solve native NumPy linear systems for the two state prices and for bond units/stock shares replicating six payoffs: bond [1,1], stock [80,130], strike-100 call [0,30], strike-100 put [20,0], up digital [0,1], down digital [1,0]. State order is always down, up. Independently compare with exact rational arithmetic. Fix absolute numerical tolerance 1e-10 in each stated unit; do not change it after seeing results.

Normalize state prices by the bond price to obtain the T-forward/risk-neutral probabilities for this deterministic-rate construction. Preserve present price, undiscounted risk-neutral expected payoff and undiscounted physical expected payoff as different quantities. Report a positive put payoff as a payoff, not realized portfolio loss or regulatory expected credit loss.

Compare two stipulated physical worlds: P(up)=3/5 and P(up)=4/5. For each, construct positive state-dependent discount factors m(s)=state_price(s)/P(s). Retain native P-weighted discounted payoff prices and P-weighted undiscounted payoffs for all six instruments. Both worlds share market prices and payoff states. Neither world is selected as empirically true. A separate exact equality control P=Q establishes that the two probability measures can coincide; do not claim they must always differ.

## Expected distinguishing evidence

The payoff matrix spans both states and determines positive state prices. That completeness concerns attainable payoffs, not identification of physical probabilities. Both stipulated worlds reproduce all six prices but differ in down-event probability, stock expected return and put expected payoff. Dividing a digital price by the bond price identifies its risk-neutral probability under these assumptions, not its physical probability. Undiscounted state-price sums need not be one.

Exact reference arithmetic uses Fraction and a closed-form two-by-two inverse, separate from NumPy's native solve. Retain replication holdings and residuals for both states, market-price differences, normalization and world-specific quantities. The general family P(up)=p, 0<p<1, with m(s)=state_price(s)/P(s), supplies an algebraic non-identification argument beyond the two examples. No claim about calibration to real data, market completeness outside the example, or predictive accuracy follows.

## Execution and retention

Commit this plan and measure.py before one CPU process, maximum 120 seconds, one attempt, no retry, network, model/provider calls or dependency installation. Use the existing local numerical environment, one thread. Record environment, source/plan SHA256, invocation, elapsed time, exit code and output. A numerical or infrastructure failure remains evidence; a correction requires a separately recorded plan. Expected controls are not model judgments.

After the run, independently check retained numbers and targeted adverse mutations without rerunning the native calculation. Inspect a concise report against the output. Identify whether model-description, numerical-evidence and valuation-comparison already express the needed requirements. Any public example is separately claimed; no new definition, publication or institutional action is part of this study.

## Primary context

[Scott Sheffield, MIT 18.440 Lecture 36](https://ocw.mit.edu/courses/18-440-probability-and-random-variables-spring-2014/4583e12e3e052256867388dd86eb5b8b_MIT18_440S14_Lecture36.pdf), slides 5–6 and 11, inspected October 6: discounted event prices define a risk-neutral probability; it need not equal ordinary event probability. Our numerical inputs, comparison design and conclusions about this synthetic construction are authored here. No external data or document is redistributed.

## Optional reproduction

This calculation is separate from the reporting program. With Python 3.12.14 and NumPy 2.5.3, run `python3 examples/pricing-probabilities/model/measure.py /tmp/open-quant-pricing-probabilities-fresh.json` from the source repository, using an unused destination and an external 120-second deadline. Preserve the original packet; compare all numerical fields and controls, excluding only timestamp, calculation duration and explicitly rebound source/plan hashes. This does not qualify agent interpretation.
