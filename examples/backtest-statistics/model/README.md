# Exception frequency, clustering and uncertainty

Fixed constructed study, October 6, 2026. One CPU process, at most 120 seconds, no retry, network, provider call, fitting or financial action. Requires Python 3.12.14, NumPy 2.5.3 and SciPy 1.18.1 for comparison with the observed environment. Preserve failed controls and all observations. Subsequent record verification does not repeat native statistical calls.

## Fixed population

Each of six constructed sequences has 250 ordered binary indicators. One denotes an exception; positions are one-based. They are not generated forecasts, actual losses or market observations. No dates, availability history, sign convention or forecast/outcome pairing are supplied, so this study cannot qualify those parts of a backtest.

| Sequence | Exception positions |
|---|---|
| isolated_five | 25, 75, 125, 175, 225 |
| clustered_five | 123 through 127 |
| boundary_cluster_five | 1 through 5 |
| zero_exceptions | None |
| isolated_ten | 13 + 25i, for i=0 through 9 |
| clustered_ten | 121 through 130 |

Retain every indicator, all exception positions, count K, sample fraction K/250, and number R of consecutive blocks of ones. A block beginning at the first position counts; the sequence is linear, not circular. These deliberately selected patterns are diagnostic cases, not estimates of a model's reliability or a test's empirical power.

## Separate statistical questions

1. **Excess frequency:** Under independent Bernoulli trials with constant null exception probability p0=1/100, calculate the one-sided probability P(X≥K) using SciPy binomtest with alternative='greater'. Compare it with the exact Fraction sum of binomial terms. This tests excess frequency only; it is not a two-sided coverage or conservatism test.
2. **Probability uncertainty:** Separately instantiate a two-sided binomial result and request its exact 95% Clopper–Pearson interval. Verify both endpoints by 100 iterations of bisection over standard-library finite binomial sums: the lower endpoint solves Pp(X≥K)=0.025, and the upper solves Pp(X≤K)=0.025. Handle K=0 and K=N explicitly. This interval is not the inversion of the selected one-sided 5% frequency test. Zero observed exceptions do not establish zero exception probability.
3. **Clustering:** Conditional on N and K under the independent, constant-probability null, all choices of K positions are equally likely. For 0<K≤N, the number of sequences with r blocks of ones is C(K−1,r−1) × C(N−K+1,r), for 1≤r≤min(K,N−K+1). Partition the K ones into r positive blocks and choose r distinct gaps among the N−K zeros; this gives the formula. Sum counts through the observed R and divide by C(N,K) for a one-sided clustering p-value. Compare the full count distribution with independent dynamic programming over sequence length, ones used, previous indicator and block count. Retain all distribution counts. For K=0, the conditional distribution is degenerate at R=0, with tail probability 1 and no timing information.

The dynamic program is checked at N=250 for K=0,5,10. Independently enumerate all 256 length-eight sequences and check the formula and dynamic program at every K=0 through 8, including the all-one boundary. This is a finite implementation control, not additional financial sampling.

Use absolute tolerance 1e-12 for native frequency probabilities and 1e-10 for interval endpoints. Integer distributions, positions and counts must match exactly. Separate 5% thresholds apply to frequency and clustering, without a combined approval rule or a familywise error claim. Reject only when the relevant p-value is strictly below 0.05. A non-rejection does not establish the null. A clustering finding challenges the independence assumption needed for the binomial calculation's inferential interpretation; retain the calculated null quantities with that limitation rather than describing them as unconditional confidence guarantees.

## Evidence and intended use

Retain source/plan hashes, input identity, command, environment, timing, all native quantities, independent references and control results. Check retained evidence with deliberate mutations to population, order, counts, alternatives, confidence endpoints, p-values and unsupported acceptance claims. Existing backtesting and outcomes-analysis contracts cover these distinctions. A worked public composition may be useful; no new definition or standard-library change is presumed.

Primary interface references inspected October 6: [SciPy binomtest](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html) and [exact proportion intervals](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html). The latter identifies the Clopper–Pearson method. The sequence choices, conditional block-count derivation and independent controls are authored here. No third-party dataset or paper text is copied.

## Optional reproduction

This owned source is an optional numerical calculation, separate from the reporting-agent program. In a fresh environment with the versions above, run `python measure.py --output /path/to/fresh-observation.json` from this directory. Use a finite 120-second process limit. The output path must not exist. Retain failed observations rather than changing the fixed inputs or replacing an unsuccessful attempt. No provider credentials or market data are needed.
