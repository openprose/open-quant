# Synthetic variance calibration

The subject is a deterministic piecewise variance curve, not an estimated market model. Time is in years. q1, q2 and q3 are instantaneous variance rates on [0,0.5], (0.5,1] and (1,2]. The selected domain is q>=0. Total variance W(T) integrates those rates. Observations are stipulated exact values W(1)=0.04 and W(2)=0.09; no empirical quotes or implied-volatility inversion are supplied.

The calibration matrix is A=[[0.5,0.5,0],[0.5,0.5,1]] and target b=[0.04,0.09]. Exact fits obey q1+q2=0.08 and q3=0.05. The original matrix has rank two and null direction [1,-1,0]. Admissible exact fits have half-year W in [0,0.04], with attainable endpoints; W(1.5)=0.065 is constant across that family. These are mathematical consequences of the stipulated model and observations, not confidence intervals or forecasts.

European ATM calls use forward and strike USD100, discount 1 and total standard deviation sqrt(W(T)). Their formula is 100*erf(sqrt(W(T)/8)) for W>=0. Zero variance gives zero price; negative variance is outside this formula's domain. A price at a valid maturity does not establish admissibility of the entire curve. Report supplied prices; fresh pricing runs are outside this reporting invocation.

S1 minimizes 0.5*||Aq-b||^2 with q>=0. S2–S5 add 0.5*(q1-q2-d)^2 for respective targets -0.06, 0, +0.06 and +0.10. Rates and targets are expressed per year; the squared-rate penalty coefficient in dimensional form is (1 year)^2. This fixed weight and the preference targets are model choices. Do not keep the same numerical weight after changing time units and call the problem unchanged.

The augmented matrix includes [1,-1,0] and has rank three. For feasible allocation targets, the zero-residual solution is q1=(0.08+d)/2, q2=(0.08-d)/2, q3=0.05. An incompatible target need not preserve exact data fit. Native status reports the solver's objective and constraints; assess original-data fit separately. All supplied values and institutions are synthetic; no institutional owner, approval or production acceptance is required or established.
