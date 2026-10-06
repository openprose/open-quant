# Numerical requirements for the shape comparison

These are illustrative house requirements, not regulatory or recommended production tolerances. They govern the numerical comparison requested by this example; they do not require the reporting executor to modify the model until it passes.

For the selected evidence snapshot, a method meets this set only if both hold:

- Maximum absolute repricing error over the selected inputs is at most **0.000001 bp**.
- Maximum absolute day-to-day forward move over the supplied measured grid is at most **2 bp**.

Compare both methods against these criteria and identify the proposed method B's finding. Preserve the finite-grid and solver-tolerance scope. Do not replace the daily measure with the separately supplied five-business-day measure or describe a small repricing residual as low model risk.
