"""One bounded synthetic hedge study; no network or agent invocation."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import time

START = time.monotonic()
import numpy as np
import scipy
from scipy.optimize import lsq_linear


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rational(value):
    return str(Fraction(value))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(Path(__file__).resolve().parents[3]):
        parser.error("Choose a fresh output directory outside the source checkout.")
    args.output.mkdir(parents=False, exist_ok=False)
    x = np.array([-2., -1., 1., 2.])
    error = np.array([1., -2., 2., -1.])
    periods = {"training": 2*x + error, "later": -x + error}
    dates = {"training": ["2026-09-21", "2026-09-22", "2026-09-23", "2026-09-24"],
             "later": ["2026-09-25", "2026-09-28", "2026-09-29", "2026-09-30"]}
    controls = []

    def check(name, observed, expected, atol=1e-8):
        passed = math.isfinite(float(observed)) and math.isclose(float(observed), float(expected), rel_tol=0, abs_tol=atol)
        controls.append({"name": name, "observed": float(observed), "expected": float(expected), "atol": atol, "passed": passed})

    native = {}
    for name, scale, period in [("training", 1, "training"), ("later_refit", 1, "later"), ("basket", 100, "training")]:
        coef, residuals, rank, singular = np.linalg.lstsq((scale*x)[:, None], periods[period], rcond=None)
        native[name] = {"solver": "numpy.linalg.lstsq", "coefficient": float(coef[0]), "scale_standard_lots": scale,
                        "residual_sums": residuals.tolist(), "rank": int(rank), "singular_values": singular.tolist(),
                        "period": period, "returned": True}
    for name, scale in [("bounded_training", 1), ("bounded_basket", 100)]:
        fit = lsq_linear((scale*x)[:, None], periods["training"], bounds=(-1/scale, 1/scale), method="trf", lsq_solver="exact", tol=1e-14, max_iter=100)
        native[name] = {"solver": "scipy.optimize.lsq_linear", "coefficient": float(fit.x[0]), "scale_standard_lots": scale,
                        "bounds": [-1/scale, 1/scale], "success": bool(fit.success), "status": int(fit.status),
                        "message": str(fit.message), "cost": float(fit.cost), "optimality": float(fit.optimality),
                        "iterations": int(fit.nit), "residuals": fit.fun.tolist(), "period": "training"}
    for name, target in [("training", 2), ("later_refit", -1), ("basket", .02), ("bounded_training", 1), ("bounded_basket", .01)]:
        check(name + ": coefficient", native[name]["coefficient"], target, 1e-10)
    check("bounded objective", native["bounded_training"]["cost"], 10)
    check("bounded basket objective", native["bounded_basket"]["cost"], 10)
    check("bounded representation", native["bounded_basket"]["coefficient"]*100, native["bounded_training"]["coefficient"], 1e-10)

    selections = [
        ("unhedged", 0., 1, Fraction(0), "fixed baseline", None),
        ("training_fit", native["training"]["coefficient"], 1, Fraction(2), "training", "2026-09-24T21:00:00Z"),
        ("bounded_fit", native["bounded_training"]["coefficient"], 1, Fraction(1), "training", "2026-09-24T21:00:00Z"),
        ("later_refit", native["later_refit"]["coefficient"], 1, Fraction(-1), "later", "2026-09-30T21:00:00Z"),
        ("basket_equivalent", native["basket"]["coefficient"], 100, Fraction(2), "training", "2026-09-24T21:00:00Z"),
        ("basket_wrong_coefficient", native["training"]["coefficient"], 100, Fraction(200), "deliberate unit error", "2026-09-24T21:00:00Z"),
    ]
    candidates = []
    for name, coefficient, scale, exact_h, selected_on, selected_at in selections:
        h = coefficient*scale
        row = {"id": name, "coefficient": coefficient, "standard_lots_per_unit": scale, "standard_lots": h,
               "exact_standard_lots_reference": rational(exact_h), "selected_on": selected_on, "selected_at": selected_at,
               "within_original_limit": abs(h) <= 1+1e-10, "periods": {}}
        for period, y in periods.items():
            residuals = y - coefficient*(scale*x)
            exact_residuals = [Fraction(int(yi))-exact_h*Fraction(int(xi)) for xi, yi in zip(x, y)]
            exact_sse = sum(v*v for v in exact_residuals)
            exact_mean = sum(exact_residuals)/4
            exact_variance = sum((v-exact_mean)**2 for v in exact_residuals)/4
            baseline = sum(Fraction(int(yi))**2 for yi in y)
            sse = float(residuals@residuals)
            measured = {"residuals_thousand_usd": residuals.tolist(), "count": 4, "sse_million_usd_squared": sse,
                        "mean_thousand_usd": float(np.mean(residuals)), "population_variance_million_usd_squared": float(np.var(residuals, ddof=0)),
                        "baseline_sse_million_usd_squared": float(y@y), "sse_reduction": 1-sse/float(y@y),
                        "exact_reference": {"residuals": list(map(rational, exact_residuals)), "sse": rational(exact_sse),
                                            "mean": rational(exact_mean), "population_variance": rational(exact_variance),
                                            "baseline_sse": rational(baseline), "sse_reduction": rational(1-exact_sse/baseline)}}
            row["periods"][period] = measured
            for i, (obs, expected) in enumerate(zip(residuals, exact_residuals)):
                check(f"{name}/{period}: residual {i}", obs, expected)
            check(f"{name}/{period}: SSE", sse, exact_sse)
            check(f"{name}/{period}: mean", measured["mean_thousand_usd"], exact_mean)
            check(f"{name}/{period}: variance", measured["population_variance_million_usd_squared"], exact_variance)
            check(f"{name}/{period}: reduction", measured["sse_reduction"], 1-exact_sse/baseline)
        candidates.append(row)

    correlations = {}
    for period, y in periods.items():
        ordinary = float(np.corrcoef(x, y)[0, 1])
        basket = float(np.corrcoef(100*x, y)[0, 1])
        correlations[period] = {"standard_lot": ordinary, "basket": basket}
        check(period + ": correlation unchanged by positive scaling", basket, ordinary, 1e-12)
    result = {"created_utc": datetime.now(timezone.utc).isoformat(), "elapsed_seconds": time.monotonic()-START,
              "source_sha256": digest(Path(__file__)), "plan_sha256": digest(Path(__file__).with_name("README.md")),
              "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
              "scope": "Synthetic hypothetical P&L calculation; no agent run, executed hedge, financial forecast or institutional acceptance.",
              "periods": {p: [{"id": f"{p}-{i+1}", "observed_at": d+"T20:00:00Z", "hedge_pnl_thousand_usd_per_lot": float(xi), "position_pnl_thousand_usd": float(yi)} for i, (d, xi, yi) in enumerate(zip(dates[p], x, y))] for p, y in periods.items()},
              "original_limit_standard_lots": [-1, 1], "native": native, "candidates": candidates, "correlations": correlations,
              "quadratic_reference": {"training": [10, -40, 50], "later": [10, 20, 20]}, "controls": controls}
    (args.output/"observations.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    passed = sum(c["passed"] for c in controls)
    print(json.dumps({"controls": len(controls), "passed": passed, "elapsed_seconds": result["elapsed_seconds"], "output": str(args.output)}))
    if passed != len(controls):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
