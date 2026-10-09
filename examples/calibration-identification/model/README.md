# Calibration fit, identification and regularization

Public reproduction plan, October 6, 2026. This is a synthetic mathematical reporting case, not a calibrated market model, empirical forecast, financial recommendation or test of agent performance.

## Fixed construction

Use nonnegative instantaneous variance rates q1, q2 and q3 on year intervals [0,0.5], (0.5,1] and (1,2]. For 0<=T<=2, total variance W(T) is the integral of that piecewise constant rate. Stipulated observed total variances are W(1)=1/25 and W(2)=9/100. The data equations are A q = b, with A=[[1/2,1/2,0],[1/2,1/2,1]] and b=[1/25,9/100]. Treat these as exact synthetic inputs; no implied-volatility inversion or empirical calibration is claimed.

A has rank two and null direction [1,-1,0]. Exact fits obey q1+q2=2/25 and q3=1/20. Nonnegativity gives q1 in [0,2/25], with both endpoints attainable. W(0.5) therefore ranges sharply from 0 to 1/25, whereas W(1.5)=13/200 for every admissible exact fit. Identification is specific to a quantity; nonunique parameters do not make every output undetermined.

Retain four exact witnesses, in order: [0,2/25,1/20], [1/25,1/25,1/20], [2/25,0,1/20] and [-1/100,9/100,1/20]. The fourth fits both observations but violates rate nonnegativity and has negative half-year total variance. Preserve it as an adverse witness; do not clip it or manufacture a Black price at negative variance.

For maturities 0.5, 1, 1.5 and 2 years, compute an ATM call with forward and strike USD100 and discount factor 1. Pass sqrt(W(T)), the total standard deviation, to QuantLib blackFormula. Independently compare with 100*erf(sqrt(W(T))/(2*sqrt(2))). Zero variance has zero ATM call value. When W is negative, retain the undefined result without calling either square-root pricing formula. A formula at another nonnegative maturity does not make the invalid entire curve admissible. These are European call values in the stipulated deterministic-variance construction, not option-market observations.

## Five fixed native solves

Use SciPy lsq_linear, bounds [0,infinity), method trf, lsq_solver exact, tol=1e-14, max_iter=100. First fit A,b alone. Then fit augmented systems adding the row [1,-1,0] and targets d=-3/50, 0, 3/50 and 1/10. This is the objective 0.5*(||Aq-b||^2+(q1-q2-d)^2), with a fixed unit numerical penalty weight. Rates and targets are expressed per year; the dimensional squared-rate penalty coefficient is (1 year)^2. The preference target is not another market observation.

For the first three augmented systems the unique exact minimizer is q1=(2/25+d)/2, q2=(2/25-d)/2, q3=1/20. They all fit the data but select different half-year outputs. Full augmented rank does not establish identification by the original data.

For d=1/10, the nonnegative optimum is [12/125,0,21/500]. Its original-data residual is [1/125,0], preference residual -1/250 and augmented objective 1/25000. This follows by setting q2=0, eliminating q3 through the second observed equation and minimizing the resulting scalar quadratic; the gradient at the active lower bound is nonnegative. Retain native diagnostics and check this separate exact certificate. Do not mistake successful minimization of the penalized objective for an exact original-data fit.

Retain success, status, message, x, cost, fun, optimality, active_mask, nit and unbounded_sol. Record original-data residuals separately from augmented residuals and the original-data fit criterion max absolute residual <=1e-10. Compare native parameters and variances with exact references within 1e-9 absolute, native objectives within 1e-10 and independent formula prices within 1e-10 USD. These are fixed observer tolerances, not institution policy. Preserve failures without changing tolerances, starting another algorithm or retrying.

## Execution and review

The retained reproduction commits this plan and measure.py before one CPU process: one attempt, at most 120 seconds, one concurrent process, no network/provider call or dependency installation, using the existing single-thread numerical environment. Retain source/plan hashes, runtime/dependency versions, elapsed time, stdout/stderr, exit state, every prescribed solve and all controls. Afterward check retained observations and adverse mutations without rerunning optimization or QuantLib. A public reporting composition requires a separate claim; existing calibration and numerical-evidence requirements are the candidate components.

## Primary implementation references

[SciPy lsq_linear](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.lsq_linear.html), inspected October 6, defines the bounded least-squares objective and returned convergence fields. [QuantLib's Black formula header](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/blackformula.hpp) describes the total-standard-deviation argument. These sources explain interfaces; the construction and exact identities above are independently derived here. Installed versions are recorded by the measurement and may differ from current online documentation.

## Reproduce separately from reporting

Use Python with NumPy 2.5.3, SciPy 1.18.1 and QuantLib 1.43, the versions selected for this reproduction. The reporting program does not authorize running this script. When calculation is separately in scope, use a fresh output path in an existing directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 examples/calibration-identification/model/measure.py /absolute/path/to/new-observations.json
```

The script rejects an existing destination. The caller supplies process supervision and the stated deadline; the script does not enforce a process-wide timeout. Keep any failure and partial evidence. Source identities and timestamps change with a new calculation; numerical agreement alone does not establish that an agent fulfilled a reproduction contract.
