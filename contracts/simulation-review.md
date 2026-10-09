# Review quantitative simulation evidence

**For agents.** Adopt [operating report](operating-report.md) and [numerical evidence](numerical-evidence.md).

The caller supplies the quantity to estimate, model and implementation identities, simulation design, observed results, uncertainty method and any precision criteria. This contract reviews supplied evidence; it does not authorize running or changing a simulation.

Identify the target quantity, units, horizon and conditioning assumptions. Explain how the reported estimate relates to that target. Preserve weighting, transformations and variance-reduction conventions that affect its meaning. A precise estimate of a different quantity does not satisfy a requirement for the requested one.

Identify the sampling units and available evidence about dependence, reused draws, random-stream construction and shared inputs. Distinguish recorded paths or rows from units supporting the uncertainty calculation. Do not treat duplicate or correlated observations as independent, or invent an effective sample size when the supplied evidence cannot establish one. For a comparison, account for shared randomness where it affects uncertainty in the difference.

Explain what a reported standard error, interval or convergence measure estimates, how it was obtained and the assumptions needed to interpret it. Preserve confidence level, denominator, sample selection and stopping rules where applicable. A formula suitable for independent random samples does not automatically apply to weighted, correlated, adaptive or quasi-random designs. Identify unavailable details that limit the conclusion.

Distinguish sampling uncertainty from discretization error, parameter uncertainty, data error and model limitations. More paths or a narrower interval does not establish that those other errors decreased. Finite observed interval coverage is not a guarantee, and a valid uncertainty method need not contain a reference value on every run.

Apply the caller's precision criteria only within their stated scope and supported assumptions. Report met, breached and unresolved findings separately from whether the simulation targets the requested quantity. Identify additional evidence needed without fabricating it, repairing source records or inferring model approval.
