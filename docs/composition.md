# Choose the requirements you need

Start with the result you want. Supply its evidence, reader, house requirements and permitted output location. Adopt only the contracts that apply.

| Result | Contract — for agents | Reusable requirements it adopts |
|---|---|---|
| Explain what a model does and how it works | [Model description](../contracts/model-description.md) | Claim evidence, institutional facts |
| Explain one supplied modeling choice | [Model decision](../contracts/model-decision.md) | Claim evidence, institutional facts |
| Interpret supplied numerical results | [Numerical evidence](../contracts/numerical-evidence.md) | Claim evidence |
| Produce full methodology documentation and supporting reports | [Documentation](../contracts/documentation.md) | Model description, numerical evidence, claim evidence, institutional facts |
| Produce fresh calculation evidence within explicit limits | [Model reproduction](../contracts/model-reproduction.md) | Numerical evidence and its claim-evidence requirements |
| Assess a selected result | [Assessment](../contracts/assessment.md) | The caller supplies the subject's requirements as the assessment basis |

For example, a short model description can use model-description.md with your model brief, evidence and house style. Add numerical-evidence.md when you also want a numerical comparison interpreted. Bind its selected results and question explicitly. The two contracts can apply to sections of one artifact; they do not require two agents, separate files or a new workflow.

A composed document must satisfy all adopted requirements. A requirement to disclose an evidence gap can be met while the underlying fact remains unknown. If another adopted contract requires that fact to be supplied, the disclosure does not make the document complete. Surface incompatible requirements rather than choosing a convenient interpretation.

The [SOFR decision example](../examples/sofr-curve/program.md) deliberately retains its smaller scope. It does not adopt the full-document or model-description contract. Reuse the component that fits your result rather than adding every available requirement.

The [authored model-description cases](../tests/cases/model-description.md) and [numerical-evidence cases](../tests/cases/numerical-evidence.md) show distinctions a reviewer should check. They are examples of intended meaning, not evidence of model performance.

For recurring quantitative operations, see [the operating-work catalog](operating-work.md). The [monitoring](../examples/monitoring-review/program.md) and [valuation](../examples/valuation-review/program.md) programs each compose two domain contracts into one report, with explicit caller policy and scope. Both are authored examples awaiting model-backed qualification.

The [full SOFR methodology example](../examples/sofr-documentation/README.md) binds the documentation contract to an explicit public technical scope. It produces a document, combined supporting records and a result record. A missing-locality case demonstrates that completing gap reporting does not supply a mandatory result. Its [dedicated assessment](../examples/sofr-documentation/assess.md) checks each artifact's requirements separately; the reference output is authored and this composition is agent-unqualified.

The [credit-loss methodology example](../examples/credit-methodology/README.md) uses the same full-document contract with different model evidence and public requirements. Its optional institutional-records mode adds requirements to supply supported facts. Disclosing the absence of those records can satisfy the public gap requirement while leaving the additional factual-entry requirements unmet; the required outcome changes even though the evidence does not.

The [two-model documentation library](../examples/documentation-library/README.md) applies those programs together. Shared definitions keep separate model/evidence bindings; the collection index accounts for both documents without merging their findings. An accurate index of unfinished work does not fulfill a requirement to produce that work. This composition remains agent-unqualified.

The [Black pricing-methodology document](../examples/pricing-methodology/README.md) applies the same documentation contract to European-option evidence. Its baseline-only selection retains the method and source mappings while withholding required native observations. Explaining a known formula does not supply an observation of what a particular implementation produced. This third document is separate from the two-model collection and remains agent-unqualified.

## Author a program for your own records

In a source checkout, a monthly review can compose [monitoring](../contracts/model-monitoring.md) and [limitations and remediation](../contracts/limitations-and-remediation.md). Supply the model revisions, reporting period, expected observations, issue records and applicable policy in `inputs/monthly-review/`. The policy identifies thresholds, missing-data treatment, required responses and closure criteria. These are caller inputs; the library does not supply an institution's policy.

Save a program such as this as `review.md` at the source-repository root. The paths below are relative to that root. This is an authoring sketch; the input directory and its contents are yours to supply.

```markdown
# Monthly model review

Execute under the caller's selected OpenProse kernel. The working root is
the directory containing this program.

Adopt contracts/model-monitoring.md and
contracts/limitations-and-remediation.md, including their adopted definitions,
for one report to the model owner.

Use only the records and policy in inputs/monthly-review/ for the model
revisions, reporting period, expected observations, issues and review criteria.
Identify missing bindings and preserve their effect on the findings.

The report must account for monitoring results and outstanding issues,
including exceptions, unsupported closure claims and unresolved evidence.
An accurately reported open issue does not prevent fulfillment of this
reporting obligation. No institutional approval is requested.

Write report.md and result.md in a fresh directory under results/monthly-review/.
Identify the requirements and evidence used, checks performed, remaining work,
reporting fulfillment and the actual output path. Preserve earlier results.

Reading supplied records and checking their arithmetic are permitted. Do not
change inputs or policy, run financial models, close issues or notify owners.
```

With the inputs supplied and an authenticated harness configured through [the running guide](running.md), the invocation is `prose run review.md`. The sketch has not been executed or qualified. For a prepared input set, start with the [monitoring example](../examples/monitoring-review/README.md).

The two contracts contribute different requirements to one report. A supported issue-closure conclusion would be an additional requested outcome, with the relevant closure criteria and evidence. Adding that outcome changes what fulfillment requires. It does not require a prescribed sequence of steps or another agent.

For a component package installed elsewhere, use the actual selected contract locations and identities. This sketch's paths assume the source checkout; examples and input records are not distributed in the component package.

The [calibration-stability example](../examples/calibration-stability/README.md) composes calibration and sensitivity review. It separates an exact fit, physical parameter uncertainty and a coordinate-dependent condition number. Its missing-perturbations case permits analytical bounds while keeping absent native execution records unresolved.
