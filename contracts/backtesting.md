# Review a risk-model backtest

**For agents.** Adopt [outcomes analysis](outcomes-analysis.md), including its adopted definitions.

The caller supplies the forecast risk measure, model and portfolio revisions, confidence level and horizon, observation population, prediction times, realized outcome definitions, exception rules and any permitted exclusions. Identify which outcome series are compared, such as actual and hypothetical P&L; do not substitute one for the other.

Apply the supplied sign convention and comparison boundary. A positive loss and a negative P&L may describe the same event. Pair each forecast with the correct subsequent outcome, preserving the evidence that the forecast was available before the evaluated period. Distinguish a valid numerical exceedance from missing, inapplicable or unavailable evidence and from any policy treatment of that evidence.

Count exceptions separately for each requested series and apply the caller's aggregation rule explicitly. A maximum of series counts, a union of exception dates and a sum of counts are different quantities. Keep the original observation population and all exclusions visible. An unsupported exclusion or waiver is not a reason to remove an exception.

Report any applicable test statistic, decision rule and uncertainty only within the supplied scope and evidence. Do not extend a short illustrative period into a regulatory annual test, infer statistical significance from an exception count alone or treat a passing test as proof of model validity. Review findings do not grant supervisory approval or authorize capital, position or model changes.
