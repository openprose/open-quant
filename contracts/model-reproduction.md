# Reproduce quantitative model results

**For agents.** Adopt [numerical evidence](numerical-evidence.md) for the comparison report, including its adopted definitions.

The caller supplies the selected implementation and input identities, required environment, permitted calculations, reference outputs, comparison policy and output scope. Resource limits must identify the allowed attempts and calculation deadline, with any permitted termination period, concurrency and other relevant limits. Identify missing authority, dependencies or comparison criteria before treating a calculation as authorized or its result as comparable.

Produce the requested calculation evidence within that scope. Record the implementation, inputs, dependency and runtime identities, invoked command or equivalent operation, attempt history and observed completion state. Preserve logs, partial outputs and failures, including failed launches and timeouts. A file's existence, process launch or normal exit does not establish completed numerical evidence. Unknown settlement remains unknown; another attempt requires remaining authority and budget.

Compare the actual result with the selected reference under the caller's policy. Preserve financial quantities, units, dates, populations, conventions and transformation scope. Distinguish exact identity from numerical agreement and from a statistical comparison; a stochastic result requires the caller's stated comparison design. Retain mismatches and unavailable comparisons without changing inputs, tolerances, seeds or the tested population to obtain agreement.

Report which selected results were reproduced, which differ and which lack evidence. Identify shared inputs or methods and what the reproduction does not cover, such as upstream acquisition, calibration suitability or institutional acceptance. Record source and output identities and the available evidence of source preservation; matching final hashes alone do not establish every action taken during execution.

Fulfillment requires the requested calculations and comparisons to meet the selected reproduction requirements. An accurate failure report does not by itself fulfill a requirement to reproduce results. A request only to investigate or report reproducibility must state that different obligation. No dependency installation, broader data retrieval, source repair, publication or financial operation is authorized unless the caller separately includes it in scope.
