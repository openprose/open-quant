# Open Quant

The reusable contracts from this repository are now maintained in **OpenProse Quant**. Start with the [public package entry for 0.3.0-rc.2](https://pkg.prose.md/releases/0.3.0-rc.2/quant/README.md). The canonical source is [packages/quant in the private application repository](https://github.com/openprose/openprose-libraries/tree/main/packages/quant).

This repository remains available with its original source, examples and history. Existing pins retain their original selections; migration does not retarget them. The guide below preserves the earlier source-checkout and qualification context, including historical candidate, branch and publication status statements.

## Historical source guide

**Open contracts for quantitative model documentation and operating work, built with OpenProse.**

Contract authoring is expressing intent by composing requirements. Open Quant provides reusable requirements for documenting a model, supporting its claims and assessing the resulting documentation. You supply the model evidence and your organization's house requirements.

The first example documents one decision in a public USD SOFR curve model: choosing an interpolation method. It produces a short decision note, not a complete model document. The reusable [full-document contract](contracts/documentation.md) is a separate scope, illustrated by [SOFR](examples/sofr-documentation/README.md), [credit-loss](examples/credit-methodology/README.md) and [Black option-pricing](examples/pricing-methodology/README.md) methodology documents.

The [two-model library example](examples/documentation-library/README.md) composes the SOFR and credit documentation programs and a collection index, preserving each model's requirements and findings. It is authored and has not received agent qualification.

This is a methodology demonstration, not a complete regulatory submission. Institutional facts are supplied by the deploying institution. Documentation assessment does not establish model soundness or institutional approval. Open Quant is an initial library, not an established industry standard.

OpenProse is not affiliated with the New York Fed. The New York Fed does not sanction, endorse, or recommend any products or services offered by OpenProse. [Data source notices](provenance/README.md#external-sources) apply to the historical SOFR inputs.

## Start with the example

Follow [the installation and composition exercise](examples/sofr-curve/COMPOSE.md). It selects public Prose CLI 0.15.0-rc.2, Claude Code 2.1.243 and an explicit Anthropic API configuration on macOS ARM64. Install, select the candidate source and review the local runtime settings before running:

```sh
prose run examples/sofr-curve/program.md
```

The program requests a fresh directory under `results/sofr-curve/` containing `note.md` and `result.md`. Inspect the actual returned paths. No numerical packages, paper downloads or private repositories are needed for this documentation task.

**Candidate status:** the example is in stacked, unmerged pull requests; the default main clone does not yet contain it. The exercise is source-checkout use, not a published component-package installation. The October 6 native rehearsal produced useful notes and also found source-attribution and completion-claim defects. [Qualification and limits](docs/qualification.md) distinguish installation, useful output and contract fulfillment.

## Understand and change it

Read [the program (for agents)](examples/sofr-curve/program.md). It binds [the model brief](examples/sofr-curve/inputs/brief.md), [computed evidence](examples/sofr-curve/inputs/results.json) and [house requirements](examples/sofr-curve/house/requirements.md) to the reusable [model-decision contract](contracts/model-decision.md). That contract composes claim-evidence and institutional-fact requirements.

[Compose a comparison-table requirement](examples/sofr-curve/COMPOSE.md#compose-a-presentation-requirement) with the original program. The reusable definitions and model inputs remain unchanged. The new entry selects both sets of requirements; assess its result against that composed agreement.

To assess a result, substitute the actual directory reported by your run:

```sh
prose run examples/sofr-curve/assess.md results/sofr-curve/YOUR-RUN-DIRECTORY
```

The assessment contract asks for findings tied to the exact subject, requirements and evidence. It permits a completed assessment to identify unmet or unresolved subject requirements. This is a separate invocation, not proof of an independent institutional review.

[Public foundations](docs/public-foundations.md) maps the library to current supervisory guidance and separates that guidance from the example's house requirements.

## Library

[Operating-work contracts](docs/operating-work.md) add model inventory, change review, monitoring, remediation, data, calibration, valuation, outcomes, backtesting, sensitivities, scenarios, P&L, vendor-model reporting, implementation review, dependence inputs and simulation evidence. Start with the small [synthetic monitoring example](examples/monitoring-review/README.md) to see how two contracts compose into one report. These new components have authored cases and offline checks; they have not received model-backed execution qualification.

| Contract | Required result |
|---|---|
| [Model description — for agents](contracts/model-description.md) | Purpose, scope, inputs, outputs, method, assumptions and limitations from supplied evidence. |
| [Model decision — for agents](contracts/model-decision.md) | A bounded account of a supplied modeling choice, alternatives, evidence and limitations. |
| [Model documentation — for agents](contracts/documentation.md) | A full document and supporting reports under supplied base and house requirements. |
| [Claim evidence — for agents](contracts/claim-evidence.md) | Support for the particular claim, preserving method, quantity, units, scope and source identity. |
| [Numerical evidence — for agents](contracts/numerical-evidence.md) | Interpretation of supplied comparisons, their conditions, tradeoffs and limits. |
| [Institutional facts — for agents](contracts/institutional-facts.md) | Visible missing institutional facts and limits on readiness claims. |
| [Documentation assessment — for agents](contracts/assessment.md) | Findings against selected requirements, with evidence gaps and assessment coverage visible. |

[Compose these contracts](docs/composition.md) with your own inputs and house requirements. Private model material can remain in your own repository; this example performs no upload to Open Quant. The selected agent/provider's data handling still applies. A private-model workflow has not been qualified here.

[The component package](PACKAGE.md) contains the reusable contracts. Runnable examples, inputs and development checks remain in this source repository; the clone-and-run flow above is unchanged. [Package preparation](docs/package.md) describes the separate delivery scopes, a versioned SOFR checkpoint and current publication status.

## Inspect without a model

[The authored reference note](examples/sofr-curve/sample-results/note.md) illustrates the requested output. It is not a recorded successful agent run. [The model source](examples/sofr-curve/model/README.md) and [source provenance](provenance/README.md) explain the retained calculations and optional reproduction.

With Python 3.10 or newer:

```sh
for script in scripts/check_*.py; do
  python3 "$script" || exit 1
done
python3 -m unittest discover -s tests -v
```

For the additional operating controls, use Node.js 18 or newer:

```sh
for script in scripts/check_*.mjs; do
  node "$script" || exit 1
done
```

Each script states the limited fixture relationships it checks. See [the test guide](tests/README.md) for their coverage.

These checks verify links, imported identities and specified numerical correspondences. They do not assess arbitrary prose, certify the financial model or establish that contract composition outperforms a baseline. [Contributing](CONTRIBUTING.md) explains how to add a contract or model example. Owned code and documentation are [MIT licensed](LICENSE); external sources retain their own terms.

The [implementation-review example](examples/implementation-review/README.md) uses observed synthetic pricing calculations to distinguish correct input mappings, reference agreement, passing identities and missing coverage. It has an authored report and deterministic controls; its report program remains agent-unqualified.

The [calibration-stability example](examples/calibration-stability/README.md) shows why an exact fit and a better matrix condition number need not establish stable physical parameters. It reuses calibration and sensitivity requirements; the worked reporting program remains agent-unqualified.
