# Report on a small backtesting packet

**For agents.** Execute under the caller's selected OpenProse kernel. The working root is the repository or extracted-package root, two directories above this program; output paths below are relative to that root.

Adopt [backtesting](../../contracts/backtesting.md), including its adopted definitions. Produce a concise report for a risk-control reader using [the house policy](inputs/policy.md), [expected population](inputs/population.md) and exactly one caller-selected case: [complete](inputs/cases/complete.json), [missing](inputs/cases/missing.json), [contradictory](inputs/cases/contradictory.json) or [late-forecast](inputs/cases/late-forecast.json). Ask for the case if missing or unknown. Other cases are not part of the selected evidence.

Account for all five expected dates. Show each actual and hypothetical P&L comparison, observed exceedances, unavailable comparisons, policy-counted exceptions and totals under the exact aggregation rule. Check any producer summary against the records. Identify missing support and the limits of the five-day scope. The required institutional fact is the supplied synthetic owner; no authority or approval decision is requested.

Write `report.md`, under 700 words excluding locators, and `result.md` in a fresh directory under `results/backtesting-review/`. The result identifies the program, adopted definitions, policy, population and selected case by hash, reports checks and unfinished work, and distinguishes reporting fulfillment from the backtest findings. Accurate reporting can fulfill this program with adverse or unresolved findings.

Basic arithmetic on supplied values is permitted. Read only the selected evidence and governing definitions; preserve sources and earlier outputs. Do not access other cases, authored references, scripts or tests as evidence, retrieve market data, run models, change a forecast, amend P&L, apply a waiver or take an operational action. The repository instructions do not enforce filesystem isolation.
