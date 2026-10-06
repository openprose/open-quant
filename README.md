# Open Quant

**Open contracts for quantitative model documentation and operating work, built with OpenProse.**

Contract authoring is expressing intent by composing requirements. Open Quant provides reusable requirements for documenting a model, supporting its claims and assessing the resulting documentation. You supply the model evidence and your organization's house requirements.

The first example documents one decision in a public USD SOFR curve model: choosing an interpolation method. It produces a short decision note, not a complete model document. The reusable [full-document contract](contracts/documentation.md) is a separate scope.

This is a methodology demonstration, not a complete regulatory submission. Institutional facts are supplied by the deploying institution. Documentation assessment does not establish model soundness or institutional approval. Open Quant is an initial library, not an established industry standard.

OpenProse is not affiliated with the New York Fed. The New York Fed does not sanction, endorse, or recommend any products or services offered by OpenProse. [Data source notices](provenance/README.md#external-sources) apply to the historical SOFR inputs.

## Start with the example

The initially checked preparation route is macOS ARM64 with Claude Code 2.1.243; other platforms are not qualified here.

Install the [Prose CLI](https://github.com/openprose/prose-cli) and a supported, authenticated agent harness. The reference commands below select Claude explicitly; they use your configured Claude account and can incur model usage. Do not put credentials in this repository.

```sh
npm install -g @openprose/prose-cli@0.15.0-rc.2 --ignore-scripts
git clone https://github.com/openprose/open-quant.git
cd open-quant
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits --dry-run run examples/sofr-curve/program.md
```

The dry run checks runtime preparation without calling a model. It does not establish authentication, contract fulfillment or successful end-to-end execution. Resolve any reported harness/version/platform issue first; see [runtime setup and qualification](docs/running.md).

Then run the example:

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/sofr-curve/program.md
```

The program requests a fresh directory under `results/sofr-curve/` containing `note.md` and `result.md`; the executor should report the actual path. Inspect both. Existing results are preserved. No numerical packages, paper downloads or private repositories are needed for this documentation task.

**Qualification:** an [actual CLI-generated note and separate assessment](examples/sofr-curve/observed-run/README.md) are now retained from a bounded OpenAI API development run. The Claude commands above and the complete attendee installation/workshop remain unqualified. One observed result does not establish reliability across harnesses or accounts. [Current evidence and limits](docs/qualification.md) separate what was checked from what remains.

## Understand and change it

Read [the program (for agents)](examples/sofr-curve/program.md). It binds [the model brief](examples/sofr-curve/inputs/brief.md), [computed evidence](examples/sofr-curve/inputs/results.json) and [house requirements](examples/sofr-curve/house/requirements.md) to the reusable [model-decision contract](contracts/model-decision.md). That contract composes claim-evidence and institutional-fact requirements.

Edit the house requirements and run again. For example, require the comparison to appear in a table with a separate limitation column. The library contracts and model inputs can remain unchanged. Changing those requirements creates a new agreement; assess the new result against that agreement.

To assess a result, substitute the actual directory reported by your run:

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/sofr-curve/assess.md results/sofr-curve/YOUR-RUN-DIRECTORY
```

The assessment contract asks for findings tied to the exact subject, requirements and evidence. It permits a completed assessment to identify unmet or unresolved subject requirements. This is a separate invocation, not proof of an independent institutional review.

[Public foundations](docs/public-foundations.md) maps the library to current supervisory guidance and separates that guidance from the example's house requirements.

## Library

[Operating-work contracts](docs/operating-work.md) add model inventory, change review, monitoring, remediation, data, calibration, valuation, outcomes, backtesting, sensitivities, scenarios, P&L and vendor-model reporting. Start with the small [synthetic monitoring example](examples/monitoring-review/README.md) to see how two contracts compose into one report. These new components have authored cases and offline checks; they have not received model-backed execution qualification.

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

[Package preparation](docs/package.md) describes the versioned candidate and its current publication status.

## Inspect without a model

[The authored reference note](examples/sofr-curve/sample-results/note.md) illustrates the requested output. It is not a recorded successful agent run. [The model source](examples/sofr-curve/model/README.md) and [source provenance](provenance/README.md) explain the retained calculations and optional reproduction.

With Python 3.10 or newer:

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -v
```

For the additional operating controls, run the check_monitoring.mjs, check_valuation.mjs, check_backtesting.mjs, check_sofr_change.mjs, check_calibration.mjs, check_vendor_inventory.mjs and check_risk_report.mjs scripts under scripts/ with Node.js 18 or newer. For example, `node scripts/check_calibration.mjs` checks the worked calibration cases.

These checks verify links, imported identities and specified numerical correspondences. They do not assess arbitrary prose, certify the financial model or establish that contract composition outperforms a baseline. [Contributing](CONTRIBUTING.md) explains how to add a contract or model example. Owned code and documentation are [MIT licensed](LICENSE); external sources retain their own terms.
