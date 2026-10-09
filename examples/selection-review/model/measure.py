"""Fixed all-null score experiment; see README.md for assumptions and limits."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
from statistics import NormalDist
import time

import numpy as np


SEED = 2026100602
REPLICATES = 256
SIZES = [1, 4, 16, 64]
TOL = 1e-12
NORMAL = NormalDist()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tail(z):
    return 0.5 * math.erfc(z / math.sqrt(2))


def family_tail(z, k):
    return -math.expm1(k * math.log1p(-tail(z)))


def first_maximum(values):
    return int(np.argmax(values))


def calculate():
    started = time.monotonic()
    ordinary = NORMAL.inv_cdf(.95)
    theory = {}
    errors = []
    for k in SIZES:
        threshold = NORMAL.inv_cdf(.95 ** (1/k))
        theory[str(k)] = {
            "ordinary_threshold": ordinary,
            "family_threshold": threshold,
            "maximum_ordinary_exceedance_probability": 1-.95**k,
            "frozen_evaluation_exceedance_probability": .05,
            "maximum_family_exceedance_probability": .05,
        }
        errors.extend([abs(tail(ordinary)-.05), abs(family_tail(threshold, k)-.05)])
    checks = {"threshold_identities_max_abs_error": max(errors),
              "threshold_identities_passed": max(errors) <= TOL,
              "tie_uses_smallest_index": first_maximum(np.array([1., 2., 2., -1.])) == 1,
              "nested_maxima_passed": True, "k1_family_identity_passed": True,
              "family_tail_not_below_raw_passed": True}
    records = []
    for replicate, parent in enumerate(np.random.SeedSequence(SEED).spawn(REPLICATES)):
        children = parent.spawn(2)
        selection = np.random.Generator(np.random.PCG64DXSM(children[0])).standard_normal(64)
        evaluation = np.random.Generator(np.random.PCG64DXSM(children[1])).standard_normal(64)
        prefixes = []
        previous_selection = previous_evaluation = -math.inf
        for k in SIZES:
            chosen = first_maximum(selection[:k])
            reselected = first_maximum(evaluation[:k])
            views = {}
            for name, index, score, selected_here in [
                ("selection_winner", chosen, selection[chosen], True),
                ("frozen_evaluation", chosen, evaluation[chosen], False),
                ("reselected_evaluation", reselected, evaluation[reselected], True),
            ]:
                z = float(score)
                raw = tail(z)
                item = {"candidate": f"M{index+1:02d}", "index": index, "z": z,
                        "raw_one_sided_tail": raw, "exceeds_ordinary_threshold": z > ordinary}
                if selected_here:
                    adjusted = family_tail(z, k)
                    item.update(independent_family_tail=adjusted,
                                exceeds_family_threshold=z > theory[str(k)]["family_threshold"])
                    checks["family_tail_not_below_raw_passed"] &= adjusted + TOL >= raw
                    if k == 1:
                        checks["k1_family_identity_passed"] &= abs(adjusted - raw) <= TOL
                views[name] = item
            checks["nested_maxima_passed"] &= (selection[chosen] >= previous_selection
                                                and evaluation[reselected] >= previous_evaluation)
            previous_selection = selection[chosen]
            previous_evaluation = evaluation[reselected]
            prefixes.append({"candidate_count": k, "views": views,
                             "evaluation_changes_candidate": chosen != reselected})
        records.append({"replicate": replicate, "selection_spawn_key": list(children[0].spawn_key),
                        "evaluation_spawn_key": list(children[1].spawn_key),
                        "selection_scores": selection.tolist(), "evaluation_scores": evaluation.tolist(),
                        "selection_scores_sha256": hashlib.sha256(selection.astype('<f8').tobytes()).hexdigest(),
                        "evaluation_scores_sha256": hashlib.sha256(evaluation.astype('<f8').tobytes()).hexdigest(),
                        "score_hash_format": "64 little-endian float64 values in candidate-index order",
                        "prefixes": prefixes})
    summary = {}
    for n, k in enumerate(SIZES):
        rows = [r["prefixes"][n] for r in records]
        views = {}
        for name in ["selection_winner", "frozen_evaluation", "reselected_evaluation"]:
            values = [r["views"][name] for r in rows]
            result = {"ordinary_exceedances": sum(v["exceeds_ordinary_threshold"] for v in values),
                      "replicates": REPLICATES, "mean_z": math.fsum(v["z"] for v in values)/REPLICATES}
            if name != "frozen_evaluation":
                result["family_exceedances"] = sum(v["exceeds_family_threshold"] for v in values)
            views[name] = result
        summary[str(k)] = {"views": views,
                           "evaluation_changes_candidate": sum(r["evaluation_changes_candidate"] for r in rows)}
    # NumPy scalar comparisons are converted for portable JSON records.
    checks = {key: float(value) if key.endswith("error") else bool(value) for key, value in checks.items()}
    return {"schema": "open-quant-selection-observations-v1", "observed_at": datetime.now(timezone.utc).isoformat(),
            "source_sha256": sha(__file__),
            "environment": {"python": platform.python_version(), "numpy": np.__version__, "platform": platform.platform()},
            "rng": {"algorithm": "PCG64DXSM", "root_seed": SEED, "replicates": REPLICATES,
                    "streams": "root.spawn(256); each replicate spawns selection/evaluation children"},
            "score_model": "independent standard normal, all candidate true effects zero",
            "candidate_ids": [f"M{i+1:02d}" for i in range(64)], "candidate_counts": SIZES,
            "tolerance": TOL, "theory": theory, "records": records, "summary": summary, "checks": checks,
            "all_checks_passed": all(v for k, v in checks.items() if k.endswith("passed") or k == "tie_uses_smallest_index"),
            "calculation_seconds": time.monotonic()-started}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = calculate()
    with args.output.open("x") as output:
        json.dump(result, output, indent=2, allow_nan=False)
        output.write("\n")
    print(json.dumps({"all_checks_passed": result["all_checks_passed"], "replicates": REPLICATES,
                      "prefix_observations": len(result["records"])*len(SIZES),
                      "calculation_seconds": result["calculation_seconds"]}))
    raise SystemExit(0 if result["all_checks_passed"] else 1)
