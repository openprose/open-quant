# Offline controls

The fixtures are authored examples with explicit field and unit bindings. Two supported numerical claims and five deliberately defective bindings cover absent evidence, a conflicting value, swapped methods, wrong units and stale source identity. Their labels were supplied by the author, not produced by a model. They are not a benchmark of executor or evaluator accuracy.

The checker compares the bindings to the retained JSON. It cannot infer a sentence's meaning, discover the correct field for an arbitrary claim, or verify the claimed source unit independently. A numerical match alone does not establish that a sentence is supported. Mutation tests demonstrate detection of changed imported bytes and changed evidence; reproduction controls reject material changes in values, dates, keys and list length.

The separate [model-description cases](cases/model-description.md) and [numerical-evidence cases](cases/numerical-evidence.md) are authored semantic review examples. Their expected interpretations are not executed by the Python tests. They distinguish useful output, missing evidence and contradictions without claiming model accuracy.

[Operating-report cases](cases/operating-reports.md) cover inventory, change, monitoring, remediation, data and calibration reporting. `node scripts/check_monitoring.mjs` checks the synthetic monitoring packet against explicit house thresholds, row identity, coverage and status contradictions. Its mutation controls are not a general contract evaluator; the authored sample report is not parsed or certified by this script.
