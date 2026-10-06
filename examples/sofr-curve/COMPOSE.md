# Add one requirement to a useful result

The example documents one choice in a public SOFR curve model. The supplied brief explains the choice and the numerical evidence; you do not need to implement a yield curve to use the contracts.

Use a fresh clone containing this example. The code is currently a candidate in unmerged pull requests; the default main branch does not yet contain it. Select the exact candidate commit from the reviewed pull request before following these instructions. This is source checkout use, not a claim that the component package is published.

## Set up the runtime once

The candidate route is macOS ARM64, Node.js 22 or newer, Prose CLI 0.15.0-rc.2 and Claude Code 2.1.243, with an Anthropic API key. The model is `claude-sonnet-5-5`, checked against the [official model documentation](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) on October 6, 2026. It is selected explicitly; this route incurs Anthropic API usage and does not use a Claude subscription login.

In your own development environment:

```sh
npm install -g @openprose/prose-cli@0.15.0-rc.2 --ignore-scripts
npm install -g @anthropic-ai/claude-code@2.1.243
```

Claude's npm package needs its installation script; do not apply the Prose command's `--ignore-scripts` option to it. Supply `ANTHROPIC_API_KEY` through your environment or secret manager, never through a committed file. Check `prose --version` and `claude --version` before proceeding.

From the repository root, review [the optional runtime settings](claude-api.toml), then copy them into your clone. They select the model, billing route, edit permissions and bounded run timeout; they contain no credentials. Preserve an existing configuration rather than overwrite it.

```sh
mkdir -p .prose
cp -n examples/sofr-curve/claude-api.toml .prose/cli.toml
prose cli config explain
prose --dry-run run examples/sofr-curve/program.md
```

Readiness means the runner can prepare the request, not that authentication or fulfillment has succeeded. A different existing configuration or account is a different selection. The [runtime guide](../../docs/running.md) explains that boundary.

## Run and inspect the original note

```sh
prose run examples/sofr-curve/program.md
```

Open the reported `note.md` and `result.md` paths. Check the selected method, both the observed benefit and the locality limitation, source locators, and missing institutional facts. The result record should identify the requirements and inputs actually used. A completion message alone is not evidence that those requirements were met.

## Compose a presentation requirement

[compare.md](compare.md) adds a small entry; its central composition is:

```markdown
Adopt [the decision-note program](program.md) and
[the comparison-table requirements](house/comparison-table.md).
Their requirements apply together to the same note and result.
```

Read [the added requirement](house/comparison-table.md): both methods and two measured properties in a table, with units, date, source locators and a short explanation of the trade-off. It describes the required result without prescribing the agent's steps.

```sh
prose run examples/sofr-curve/compare.md
```

Inspect the new output beside the original. The table is the added requirement; the original evidence, attribution, limitations and institutional-gap requirements still apply. Edit the table requirement to express your own presentation need and run again if you want another iteration. Preserve each result and the agreement used to produce it.

## Assess the actual composition

Substitute the real result directory from the comparison run:

```sh
prose run examples/sofr-curve/assess.md results/sofr-curve/YOUR-COMPARISON-RUN examples/sofr-curve/compare.md
```

The final argument tells the assessor which composed agreement to inspect. Omit it only for the original base program. This separate invocation incurs additional usage. Inspect the findings and their evidence, including any unresolved execution effects; the assessor's own conclusion also needs review. Model assessment is not institutional approval.

The public [component catalog](../../PACKAGE.md) contains reusable documentation and operating requirements. These examples use the definitions in your checkout; fetching a package elsewhere does not replace them automatically. Source availability, a published package and a qualified workflow are separate milestones.
