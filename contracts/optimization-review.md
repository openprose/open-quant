# Review quantitative optimization evidence

**For agents.** Adopt [operating report](operating-report.md) and [numerical evidence](numerical-evidence.md), including their adopted definitions.

The caller supplies the selected problem, implementation and input identities, candidate results, solver diagnostics, comparison evidence and acceptance criteria. Identify the decision variables and their domains, objective direction and units, constraints, and relevant time or population scope. Missing problem definitions or diagnostics limit the corresponding conclusions.

Establish which problem the implementation actually represents. Preserve variable and input ordering, units, scaling, bounds and constraint identities. Distinguish the original problem from omitted, relaxed, transformed or substituted requirements; a successful solution to a different problem does not establish fulfillment of the original requirements.

Account for every selected constraint at each required candidate using the caller's tolerances and original meanings. Distinguish observed feasibility, violations and unavailable checks. Preserve the exact candidate being assessed: clipping, renormalization, rounding or other changes produce a revised candidate whose requirements must be checked again. A rounded display alone does not establish that the underlying candidate changed.

Separate native termination status, candidate feasibility and evidence of optimality. Report the objective in the requested units and identify the basis for any bound, gap or reference comparison. Distinguish local or stationary findings from a supported global conclusion, including the assumptions required by a certificate or reference. Neither a solver success flag nor a small rescaled objective establishes the requested accuracy. A lower objective at an infeasible point is not an improvement to a constrained solution.

Retain failed attempts and the evidence they provide without promoting a feasible candidate to an acceptable optimum or treating unsuccessful termination as proof of infeasibility. Identify unmet or unresolved criteria and their material limits. This review does not authorize changing constraints, rerunning a solver, selecting a different objective, implementing allocations or undertaking another financial action unless separately included in the caller's scope.
