# SOFR repricing review — authored reference

This illustrates expected findings; it is not an agent output or an assessment certificate.

For September 18, 2026, the calibration population comprises two deposit anchors and 20 selected OIS tenors: 22 instruments per method, 44 method/instrument comparisons. The source's 9M and 25Y tenors are explicitly excluded; no holdout repricing is supplied. O/N and T/N use the retained fixing as their anchor target.

A uses QuantLib log-linear discount interpolation. B uses the supplied Hagan–West monotone-convex implementation with a positivity collar, solving OIS par-rate residuals over discrete forwards. QuantLib supplies shared instrument schedules; B has its own pricing implementation. Source settings and a completed calculation do not establish uniqueness or parameter stability. The B source checks a residual bound after the solver returns, rather than using its success flag as the sole acceptance condition.

**Complete case.** All 44 supplied residuals are within the illustrative absolute 0.000001 bp limit. A's largest displayed absolute residual is 3.860e-09 bp at 6M; B's is 2.755e-10 bp at T/N. Full-precision summary maxima agree at the CSV's reported precision. Both methods meet this input-fit criterion. Equal six-decimal percentage rates do not imply exact zero residual: their display discards the differences measured in the residual columns. These residuals concern solver accuracy on calibration inputs, not superior predictive performance.

**Missing case.** The 6M row is unavailable: 21 of 22 instruments, or 42 of 44 method/instrument comparisons, are present. Available residuals are within limit, but neither method has complete item-level support. The retained aggregate summary does not fill that gap. Obtain the identified missing evidence; do not recreate it from the complete case while assessing this packet.

**Contradictory case.** A's altered 6M residual is +0.002 bp, 2,000 times the limit. It also conflicts with both rounded percentage rates, whose equal displayed values permit at most approximately 0.0001 bp difference from rounding, and with the unchanged summary maximum. Report the recorded breach and conflict. The supplied packet cannot support an overall all-clear for A, and the altered row does not prove the actual model produced it. B's 22 comparisons retain their supported input-fit finding. Reconcile the disputed source against authentic calculation evidence before accepting A's reported fit.

The October 6 reproduction establishes the complete table conditional on retained derived quotes and fixing. It did not rerun raw quote derivation. No case establishes model approval, independent validation, out-of-sample performance or institution-specific acceptance. Accurate reporting of the missing or conflicting evidence can fulfill the reporting obligation.

Sources: selected repricing CSV by instrument and method; quotes.csv used_in_bootstrap and quote_pct fields; fixing sofr_percent; results.json repricing_max_abs_error_bp; bootstrap.py repricing and CSV formatting; hagan_west.py bootstrap; the selected policy and reproduction receipt. An actual execution must supply its own artifact identities and result; this authored illustration does not supply them.
