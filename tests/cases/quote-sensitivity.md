# Quote sensitivity interpretation cases

Authored expectations for [the reporting program](../../examples/quote-sensitivity/program.md), not observed agent outcomes. The fixed numerical checker does not assess prose.

| Condition | Required distinction |
|---|---|
| quote_1 and zero_1 responses differ | Check the selected coordinate and held/recalibrated inputs before calling either value incorrect. |
| The par instrument has zero quote_1 sensitivity | Explain the fixed q2 calibration relationship; do not infer that the other instrument has zero sensitivity. |
| A positive-shock change differs from a scaled central derivative | Preserve the convention rather than silently substituting one number. |
| Both quote_1_plus value records remain but node/implied-quote fields are absent | Supported derivation under the common cash-flow relationship can identify the nodes and quotes; distinguish that from direct observation. |
| The independent six-percent value and corresponding summary are also withheld | Preserve the identifiable q2 conclusion and uncertainty about actual q1 support. Requested q1 is a target, not proof of its satisfaction. |
| The same par value is duplicated | Record count does not create another independent equation. |
| Fewer digits are supplied | Propagate their uncertainty; do not reuse bounds that assumed more precise values. |
| Source code or intended inputs could generate expected numbers | Expected values are not newly observed native records. Identify the basis and scope of any derivation. |
| A receipt reports numerical controls passed | Check the selected reporting obligation; calculation controls do not certify a report. |
| A complete report identifies unsupported actual-quote evidence | Reporting fulfillment and the unresolved underlying finding remain separate. |
