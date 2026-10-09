# Two-interval synthetic variance calibration

The model has variance rate a on [0,1] and b on (1,1+epsilon], with time in years. Its two total-variance observations satisfy q1=a and q2=a+epsilon*b. Rates are variance/year; total variances are dimensionless. Nonnegative a and b are required for a variance interpretation. These synthetic durations are not calendar dates or market observations.

Use baseline a=0.04 and b=0.09 at epsilon=1, 1/12, 1/365 and 1/3650. For each spacing, the stipulated input set permits independent changes of up to eta=0.00004 in each total variance. No statistical distribution, estimated error bar or institutional tolerance is supplied.

The expected native cases at each spacing are baseline, common-up (+eta,+eta), common-down (-eta,-eta), steepen (-eta,+eta) and flatten (+eta,-eta). At epsilon=1/3650 also expect admissible-boundary with q1=q2=0.04. This gives twenty-one requested cases, with two native solutions per case.

Physical coordinates (a,b) use matrix [[1,0],[1,epsilon]]. Integrated coordinates (a,u), where u=epsilon*b, use [[1,0],[1,1]]. Each case is solved in both coordinates; the integrated result is mapped back to physical rates. Four pairs of native infinity-norm matrix condition numbers are supplied. The infinity norm is the largest absolute row sum; the condition number is norm(A)*norm(inverse(A)). This quantity depends on the parameter coordinates and norm.

The supplied relationship permits analytical conclusions even when native records are absent. An analytical value is not an observation of native execution. The receipt identifies one NumPy 2.5.3 calculation and its source/record hashes; this reporting task requests no fresh reproduction.
