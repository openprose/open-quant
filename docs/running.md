# Runtime setup and first-run limits

The library is Markdown. The public Prose CLI supplies the selected OpenProse kernel to an installed agent harness; it does not parse these contracts into a deterministic interpreter. Use a fresh clone outside a developer workspace whose automatic agent instructions might affect the task.

## Reference route

The README selects released CLI `0.15.0-rc.2`, Claude, model alias `haiku` and permission mode `acceptEdits` with native profile `claude-workspace-tools`. This profile exposes file and shell tools while disabling user/project/local settings sources; it does not grant unrestricted tool permissions. The initially checked platform is macOS ARM64 and the admitted Claude version is 2.1.243. Other platforms are not qualified here. Install and authenticate a native Claude version admitted by that CLI. Native admission and platform restrictions still apply; inspect `prose cli harness list` and the dry-run result rather than assuming the latest installed harness works. The reference route uses the existing Claude subscription/login, not a silent API-key substitution. For another billing route select its documented auth profile explicitly. See the CLI's [credential guide](https://github.com/openprose/prose-cli/blob/main/docs/api-credentials.md).

A dry run resolves the kernel and checks preparation without dispatching a model. It may contact the public package service. Success does not verify account access or semantic fulfillment. The installed harness is a prerequisite: installing the Prose npm package alone does not install and authenticate an agent.

Ordinary published CLI startup resolves the current public kernel. Pinning the CLI version does not freeze the kernel. Retain the observed kernel identity with any qualified run. A runtime mismatch is not solved by pointing at an unrelated private development build or silently downgrading a shared harness. This initial example has no private kernel or repository prerequisite.

## Working scope

Run from the repository root. The program directs the executor to the selected sources and writes fresh results under results/. Source files and prior runs remain unchanged. Native `acceptEdits` is a harness permission choice, not a filesystem confinement guarantee. Use a suitable isolated environment for stronger enforcement.

To assess a generated note, pass the actual result directory after examples/sofr-curve/assess.md. The evaluator checks that recorded requirement/input identities still match; if they do not, supply the original snapshot or make a separately identified new assessment. Sample outputs and test references are not execution evidence.

## Before describing this as a working public journey

Record the installed CLI and harness versions, actual model identity, kernel identity, input hashes, permissions, native completion, output inspection and available usage. Rehearse the exact first run and house-requirement change on every platform claimed. No elapsed-time or success-rate promise follows from the current offline checks.

The full methodology-document contract is available for a caller that supplies all its base, house and report inputs. It is not invoked by the shorter SOFR program. Neither output grants institutional approval.
