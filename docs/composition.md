# Choose the requirements you need

Start with the result you want. Supply its evidence, reader, house requirements and permitted output location. Adopt only the contracts that apply.

| Result | Contract — for agents | Reusable requirements it adopts |
|---|---|---|
| Explain what a model does and how it works | [Model description](../contracts/model-description.md) | Claim evidence, institutional facts |
| Explain one supplied modeling choice | [Model decision](../contracts/model-decision.md) | Claim evidence, institutional facts |
| Interpret supplied numerical results | [Numerical evidence](../contracts/numerical-evidence.md) | Claim evidence |
| Produce full methodology documentation and supporting reports | [Documentation](../contracts/documentation.md) | Model description, numerical evidence, claim evidence, institutional facts |
| Assess a selected result | [Assessment](../contracts/assessment.md) | The caller supplies the subject's requirements as the assessment basis |

For example, a short model description can use model-description.md with your model brief, evidence and house style. Add numerical-evidence.md when you also want a numerical comparison interpreted. Bind its selected results and question explicitly. The two contracts can apply to sections of one artifact; they do not require two agents, separate files or a new workflow.

A composed document must satisfy all adopted requirements. A requirement to disclose an evidence gap can be met while the underlying fact remains unknown. If another adopted contract requires that fact to be supplied, the disclosure does not make the document complete. Surface incompatible requirements rather than choosing a convenient interpretation.

The [SOFR decision example](../examples/sofr-curve/program.md) deliberately retains its smaller scope. It does not adopt the full-document or model-description contract. Reuse the component that fits your result rather than adding every available requirement.

The [authored model-description cases](../tests/cases/model-description.md) and [numerical-evidence cases](../tests/cases/numerical-evidence.md) show distinctions a reviewer should check. They are examples of intended meaning, not evidence of model performance.

For recurring quantitative operations, see [the operating-work catalog](operating-work.md). The [monitoring](../examples/monitoring-review/program.md) and [valuation](../examples/valuation-review/program.md) programs each compose two domain contracts into one report, with explicit caller policy and scope. Both are authored examples awaiting model-backed qualification.

The [full SOFR methodology example](../examples/sofr-documentation/README.md) binds the documentation contract to an explicit public technical scope. It produces a document, combined supporting records and a result record. A missing-locality case demonstrates that completing gap reporting does not supply a mandatory result. Its [dedicated assessment](../examples/sofr-documentation/assess.md) checks each artifact's requirements separately; the reference output is authored and this composition is agent-unqualified.
