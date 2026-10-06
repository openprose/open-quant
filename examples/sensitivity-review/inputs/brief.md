# Synthetic forward-sensitivity review

Review SENSITIVITY-2026-10-06, three hypothetical receiving units of European calls considered separately. ATM has F=100,K=100,sigma=0.3,T=2,r=0.05. OTM changes F to 60. Short-ATM has F=K=100,sigma=0.2,T=1/365,r=0.05. F and K are USD, T is years; each case uses discount exp(-r*T) and standard deviation sigma*sqrt(T). The cases are alternatives, not an aggregated portfolio.

Each case has symmetric forward bumps h=1e-6,1e-4,0.01,0.1,1,5 USD. Strike, volatility, maturity and discount remain fixed. No recalibration, spot conversion, smile dynamics or joint shock is modeled. The factor is forward, not spot or a rate. Prices are USD PV; forward delta is USD PV per USD forward and forward gamma is USD PV per squared USD forward. Up/down premium changes are USD PV for the specified finite shocks.

The record includes QuantLib values and analytic forward derivatives and independent Python closed-form references under the same Black assumptions. This is a comparison of implementations, not independent economic models. Central delta is (Vplus−Vminus)/(2h); central gamma is (Vplus−2Vbase+Vminus)/h². Each is reported using unrounded prices and prices rounded to two decimals. All tested steps are retained; no favorable-step selection occurred.

The receipt records an actual CPU calculation and authored projection. It does not certify agent performance, market relevance, institutional suitability or a hedge recommendation. No market calibration, real portfolio, realized P&L or institutional approval evidence is supplied.
