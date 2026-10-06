# Review model sensitivity evidence

**For agents.** Adopt [operating report](operating-report.md) and [numerical evidence](numerical-evidence.md).

The caller supplies the model revision, base inputs and outputs, perturbations and resulting outputs, risk-factor definitions, calculation conventions and review criteria. Identify whether each result is a supplied model run, a local approximation or a derived calculation.

Explain which inputs changed, by how much, in which units, and which inputs were held fixed or recalibrated. Preserve the sign and scale convention for sensitivities, including whether a quoted result is a derivative, a change for a specified shock, or a normalized measure. A basis-point shock to a rate is distinct from a percentage change in that rate.

Account for requested factors and perturbations, including failed or absent results. Compare like-for-like outputs, report nonlinear or asymmetric responses visible in the evidence, and distinguish single-factor from joint perturbations. Do not assume individual effects add when the supplied model response includes interactions or the evidence is insufficient.

State the range over which the evidence supports the conclusion. A local sensitivity does not establish behavior under a large stress, and a finite set of tested shocks is not a bound on all possible losses. Model reruns or new shocks require the caller's explicit execution scope.
