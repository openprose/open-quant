# Runtime setup and first-run limits

The library is Markdown. The public Prose CLI supplies the selected OpenProse kernel to an installed agent harness; it does not parse these contracts into a deterministic interpreter. Use a fresh clone outside a developer workspace whose automatic agent instructions might affect the task.

Run the examples from the complete source checkout. The reusable component package contains contracts only; fetching it does not install these example programs or their inputs. [Package and example delivery](package.md) gives a pinned source checkpoint and keeps the two scopes explicit.

## Reference route

The README selects released CLI `0.15.0-rc.2`, Claude, model alias `haiku` and permission mode `acceptEdits` with native profile `claude-workspace-tools`. This profile exposes file and shell tools while disabling user/project/local settings sources; it does not grant unrestricted tool permissions. The initially checked platform is macOS ARM64 and the admitted Claude version is 2.1.243. Other platforms are not qualified here. Install and authenticate a native Claude version admitted by that CLI. Native admission and platform restrictions still apply; inspect `prose cli harness list` and the dry-run result rather than assuming the latest installed harness works. The reference route uses the existing Claude subscription/login, not a silent API-key substitution. For another billing route select its documented auth profile explicitly. See the CLI's [credential guide](https://github.com/openprose/prose-cli/blob/main/docs/api-credentials.md).

A dry run resolves the kernel and checks preparation without dispatching a model. It may contact the public package service. Success does not verify account access or semantic fulfillment. The installed harness is a prerequisite: installing the Prose npm package alone does not install and authenticate an agent.

Ordinary published CLI startup resolves the current public kernel. Pinning the CLI version does not freeze the kernel. Retain the observed kernel identity with any qualified run. A runtime mismatch is not solved by pointing at an unrelated private development build or silently downgrading a shared harness. This initial example has no private kernel or repository prerequisite.

## Runner options and case selection

Place runner options before the language command `run`. Arguments after `run` identify the program and the caller's selected case, mode or output path. For example, this prepares the P&L example's `missing-corner` invocation without starting a model:

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits --dry-run run examples/pnl-attribution/program.md missing-corner
```

Keep `--dry-run` before `run`; appending it after the program or case passes it as language input and does not enable the runner's dry-run mode. Quote any path containing spaces so the shell passes it as one argument.

Preparation checks the selected runtime. The runner preserves the program and case arguments without interpreting them. It does not check that the program file exists, that its case is valid, that required input records are complete or that the result will satisfy the contract. Choose a case from the example's README and inspect the executor's actual result after an authorized run.

An isolated October 6 preparation check used released CLI 0.15.0-rc.2 and native Claude 2.1.243 on macOS ARM64. It resolved kernel 0.1.0-rc.1 and stopped at `HARNESS_NEEDS_AUTH` with `wouldStartModel: false`; the source snapshot was unchanged. The fresh Claude configuration was deliberately unauthenticated. This establishes the preparation boundary and an authentication prerequisite, not a completed attendee execution.

## Working scope

Run from the repository root. The program directs the executor to the selected sources and writes fresh results under results/. Source files and prior runs remain unchanged. Native `acceptEdits` is a harness permission choice, not a filesystem confinement guarantee. Use a suitable isolated environment for stronger enforcement.

To assess a generated note, pass the actual result directory after examples/sofr-curve/assess.md. The evaluator checks that recorded requirement/input identities still match; if they do not, supply the original snapshot or make a separately identified new assessment. Sample outputs and test references are not execution evidence.

## Before describing this as a working public journey

Record the installed CLI and harness versions, actual model identity, kernel identity, input hashes, permissions, native completion, output inspection and available usage. Rehearse the exact first run and house-requirement change on every platform claimed. No elapsed-time or success-rate promise follows from the current offline checks.

The [full methodology-document example](../examples/sofr-documentation/README.md) supplies an explicit public scope, base/house requirements and source bindings for the default documentation contract. It is separate from the short SOFR program and has not been run by an agent. Neither output grants institutional approval.

## Assess an operating report

The worked operating reports in the [operating-work catalog](operating-work.md) produce `report.md` and `result.md`. Their common [assessment entry point](../examples/assess-report.md) takes the subject program, actual result directory and the case or mode used for that invocation. For example, replace `YOUR-RUN` with the directory reported by the monitoring execution:

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/assess-report.md examples/monitoring-review/program.md results/monitoring-review/YOUR-RUN complete
```

This is a separate model invocation with its own usage. The new entry point has not received model-backed qualification. Supply the original requirement/input snapshot if current files differ; current files must not silently replace the old agreement. A content finding and evidence about execution behavior are separate. Read the assessment's coverage and its own fulfillment claim, not only its conclusion about the subject.

For another operating example, substitute its program, actual result directory and original case or mode. For the original SOFR `note.md` output, continue to use `examples/sofr-curve/assess.md` instead.

## Assess a full methodology document

The full example produces document.md, reviews.md and result.md. Use its dedicated entry point with the actual result directory and original case:

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/sofr-documentation/assess.md results/sofr-documentation/YOUR-RUN complete
```

Replace complete with missing-locality when that was the subject's selection. The common operating-report entry expects a different artifact set; it is not the binding for this full document. This execution and assessment route remains unqualified.

## Observed OpenAI development route

The October 6 development run used released CLI 0.15.0-rc.2 and the optional `agents-sdk` harness, with an explicit OpenAI API credential route. Follow the CLI's [Agents SDK setup](https://github.com/openprose/prose-cli/blob/1bb5d356acd682222deffc70357bf2ad4528755a/docs/agents-sdk-adapter.md) to understand its separate launcher/dependency prerequisites. Installing the CLI alone does not supply this harness.

With an admitted `prose-agents-sdk` executable on PATH and your OpenAI API credential supplied through the environment, the selected command was:

```sh
prose --harness agents-sdk --auth-profile openai-api-key --model gpt-5.6-luna --output-contract native --native-max-turns 10 --native-timeout 570s --timeout 600s run examples/sofr-curve/program.md
```

For assessment, replace the final program path with `examples/sofr-curve/assess.md` and append the actual result-directory path. Each invocation incurs separate model usage; native turns are model requests within that invocation. `native` settlement reports harness completion, not requirement fulfillment.

The observed research setup additionally used a container and disabled provider transport retries; an ordinary native installation is a different configuration. The requested model alias and rates were checked October 5, 2026 against the [official model page](https://developers.openai.com/api/docs/models/gpt-5.6-luna). These records establish one development example, not a fresh-machine qualification or a recommendation that this model is optimal.

## Reverse-stress reporting

From the source repository, run `prose run examples/reverse-stress/program.md complete`, replacing `complete` with `missing-candidate` or `contradictory` for the other evidence selections. The [example guide](../examples/reverse-stress/README.md) gives the corresponding assessment invocation and qualification limits. The reporting program reads the supplied results; its optional numerical reproduction is separate.

## Pricing probabilities

From the source repository, run `prose run examples/pricing-probabilities/program.md complete`, replacing `complete` with `missing-world` or `contradictory` for the other selections. The [example guide](../examples/pricing-probabilities/README.md) provides the assessment invocation. The report explains retained evidence; its optional numerical reproduction is a separate operation. Agent execution remains unqualified.

## Exposure/default dependence

From the source repository, run `prose run examples/exposure-default/program.md complete`, replacing `complete` with `missing-joint` or `contradictory` for the other selections. The [example guide](../examples/exposure-default/README.md) provides the assessment invocation and distinguishes prepared-evidence reporting from optional numerical reproduction. Agent execution remains unqualified.

## Calibration identification

From the source repository, run `prose run examples/calibration-identification/program.md complete`, replacing `complete` with `missing-allocation` or `contradictory` for the other selections. The [example guide](../examples/calibration-identification/README.md) gives its assessment invocation. Reporting reads prepared evidence; optional numerical reproduction is separate. Agent execution remains unqualified.
