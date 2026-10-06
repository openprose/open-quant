# Calibration fit and stability

An exactly fitted, uniquely solved calibration can remain sensitive to its inputs. A change of coordinates can improve a matrix condition number without shrinking uncertainty in the physical parameter. This example composes the existing calibration and sensitivity contracts to explain those distinctions.

The [program](program.md) produces one report and result record from a selected evidence packet. It permits arithmetic and derivation, without prescribing a workflow or authorizing native model runs.

| Selection | Evidence |
|---|---|
| `complete` | Twenty-one cases, forty-two native solutions and eight condition numbers. |
| `missing-perturbations` | Four baseline cases and all eight condition numbers; perturbation and boundary native records are absent. |
| `contradictory` | Complete records with five producer claims to assess. |

From the source root with the [authenticated runtime](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/calibration-stability/program.md complete
```

Replace complete with one selected case. For a separate assessment, supply the actual result path and original selection:

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/assess-report.md examples/calibration-stability/program.md results/calibration-stability/YOUR-RUN complete
```

The [authored reference](sample-results/report.md) covers complete only. All native repricing residuals are zero, but the shortest-spacing admissible variance-rate interval is [0, 0.382] under the stipulated input set. Rescaling lowers the matrix condition number from 7,302 to 4 while preserving physical uncertainty. These are synthetic linear-algebra findings, not an empirical forecast or novel calibration method.

In missing-perturbations, the brief still supports derivation of sharp mathematical bounds. That does not recover an observation of native execution. This distinction is intentional; neither a missing field nor a successful process should determine every finding at once.

[Plan](model/PLAN.md), [owned source](model/measure.py), [retained observations](model/observations.json) and [receipt](receipt.json) preserve one prespecified development calculation. They were copied unchanged; no new public reproduction or reporting-agent run is claimed. Calculation reproduction requires separate execution limits and NumPy 2.5.3. The reporting task itself needs no numerical dependency.

Run `python3 scripts/check_calibration_stability.py` for fixed-record projection, arithmetic and mutation checks. [Interpretation cases](../../tests/cases/calibration-stability.md) are authored expectations. These checks do not evaluate arbitrary prose or establish agent fulfillment, production calibration suitability, workshop readiness or operating savings.
