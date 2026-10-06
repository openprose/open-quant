# Permitted source register

This register binds reporting evidence, not additional operating requirements. Read the selected numerical case and the shared sources below. Links inside evidence are locators; they do not enlarge permission to read other results, papers or historical documents. Material outside this register cannot supply the requested account.

| Source | Permitted use and limits |
|---|---|
| [Developer brief](../../sofr-curve/inputs/brief.md) | Model purpose, A/B identity, selected method and its stated rationale. A reason is attributed to the developer, not promoted to a universal model ranking. |
| Numerical case selected by the program | Historical quantitative observations, with their field identities. In missing-locality, use only the projected JSON; do not read the original results or other examples to supply the withheld values. |
| [Derived quotes](../../sofr-curve/inputs/quotes.csv) and [fixing](../../sofr-curve/inputs/sofr-fixing.json) | Input fields, selection flags and dated fixing. Raw transactions and quote-derivation execution are outside this supplied scope. Post-as-of fields in the fixing are not the as-of input. |
| [Bootstrap source](../../sofr-curve/model/bootstrap.py) and [interpolator source](../../sofr-curve/model/hagan_west.py) | Actual implementation, conventions and definitions of metrics. Source inspection is permitted; execution is not. External paper references in comments do not supply the contents of those papers. |
| [Imported-source manifest](../../../provenance/import.json) and [source notices](../../../provenance/README.md) | Ownership, original source identities, imported bytes and limitations of the supplied material. Reading the manifest does not authorize reading a nonselected numerical case. |
| [Numerical reproduction receipt](../../../provenance/reproduction/2026-10-06.json) | Evidence that the earlier full numerical record was reproduced under its stated tolerance and dependency identities. It is not a report written by this executor or a source for withheld numerical values. |
| [Institutional facts](../../sofr-curve/inputs/institutional-facts.md) | The selected fact categories and their absence from this public example. The original decision-note presentation instruction does not govern this full document. |

For locality, the source's `d4` and `d6` are the actual 4Y/6Y instrument pillar dates, 2030-09-25 and 2032-09-24. The inside interval includes both endpoints; outside excludes them. The name does not mean nominal Act/365F times 4.0 and 6.0. This explanation locates the metric definition; it does not supply a missing observed value.
