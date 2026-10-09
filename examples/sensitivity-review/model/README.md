# Reproduce forward sensitivities and price rounding

The owned source measures three synthetic European calls at six symmetric forward bumps, holding strike, volatility, maturity and discount fixed. It compares QuantLib prices and analytic forward Greeks with Python closed-form arithmetic, then derives central delta/gamma from unrounded and cent-rounded prices. Thirty-six derivative views are retained without selecting favorable steps.

The development environment is Python 3.12.14 and QuantLib 1.43. From the source root, use a fresh output file:

```sh
mkdir -p results
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python examples/sensitivity-review/model/measure.py results/sensitivity-observations.json
```

The script refuses overwrite and preserves observations before exiting nonzero for failed controls. Inputs are ATM (F=100,K=100,sigma=0.3,T=2,r=0.05), OTM (F=60 with other ATM inputs), and short-ATM (F=K=100,sigma=0.2,T=1/365,r=0.05). Each is one receiving unit; price and forward/strike are in USD. Standard deviation is sigma*sqrt(T), discount is exp(-r*T). Bumps are 1e-6,1e-4,0.01,0.1,1,5 USD forward.

Independent reference formulas use the same assumed Black model, not an independent economic model. QuantLib price and analytic derivative agreement uses absolute 1e-10 tolerances. Rounding is Python round(price,2), with half-cent error control plus 1e-12 allowance. Central delta is (Vplus−Vminus)/(2h), gamma is (Vplus−2Vbase+Vminus)/h². Quantization-only envelopes are epsilon/h and 4*epsilon/h² with epsilon=0.005 USD and floating allowance 1e-7*max(1,bound). They do not bound truncation or model error.

The illustrative absolute derivative tolerance is 1e-4 separately in each metric's units. It is not a financial standard or experiment pass gate. Every tested step is retained; no universal optimal bump or hedge follows. This developer reproduction is separate from the reporting invocation, which may not use this source or another packet to reconstruct withheld observations.
