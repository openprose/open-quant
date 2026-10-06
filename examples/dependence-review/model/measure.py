"""Fixed synthetic correlation controls; see README.md for scope and limits."""
import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import platform
import time

import numpy as np
import numpy.linalg._umath_linalg as native_linalg


TOL = 1e-12
LABELS = ["A", "B", "C"]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def correlation(ab, ac, bc):
    return np.array([[1.0, ab, ac], [ab, 1.0, bc], [ac, bc, 1.0]])


def inspect(matrix):
    symmetry_error = float(np.max(np.abs(matrix - matrix.T)))
    if symmetry_error > TOL:
        raise ValueError("Cannot use a symmetric eigensolver to certify asymmetric input")
    values, vectors = np.linalg.eigh(matrix)
    reconstructed = (vectors * values) @ vectors.T
    pairs = []
    for i, j in itertools.combinations(range(3), 2):
        pairs.append({"variables": [LABELS[i], LABELS[j]],
                      "eigenvalues": np.linalg.eigvalsh(matrix[np.ix_([i, j], [i, j])]).tolist()})
    try:
        lower = np.linalg.cholesky(matrix)
        cholesky = {"succeeded": True,
                    "reconstruction_max_abs_error": float(np.max(np.abs(lower @ lower.T - matrix)))}
    except np.linalg.LinAlgError as error:
        cholesky = {"succeeded": False, "error": str(error)}
    return {"matrix": matrix.tolist(), "symmetry_max_abs_error": symmetry_error,
            "diagonal_max_abs_error": float(np.max(np.abs(np.diag(matrix) - 1))),
            "maximum_absolute_entry": float(np.max(np.abs(matrix))),
            "eigenvalues": values.tolist(), "positive_semidefinite_at_tolerance": bool(values[0] >= -TOL),
            "positive_definite_above_tolerance": bool(values[0] > TOL),
            "eigen_reconstruction_max_abs_error": float(np.max(np.abs(reconstructed - matrix))),
            "pair_blocks": pairs, "cholesky": cholesky}


def calculate():
    started = time.monotonic()
    checks = {}

    def check(name, actual, expected):
        error = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
        checks[name] = {"max_abs_error": error, "passed": error <= TOL}

    invalid = correlation(0.9, 0.9, -0.9)
    matrices = {"identity": np.eye(3), "singular": np.ones((3, 3)), "inconsistent": invalid}
    vector = np.array([-1.0, 1.0, 1.0]) / np.sqrt(3)
    quadratic = float(vector @ invalid @ vector)
    check("inconsistent_spectrum", np.linalg.eigvalsh(invalid), [-0.8, 1.9, 1.9])
    check("negative_quadratic_form", quadratic, -0.8)
    for i, j in itertools.combinations(range(3), 2):
        check(f"pair_spectrum_{i}_{j}", np.linalg.eigvalsh(invalid[np.ix_([i, j], [i, j])]), [0.1, 1.9])

    raw = [[-1, -1, -1], [-1, 1, 1], [1, -1, 1], [1, 1, -1],
           [-10, -10, None], [10, 10, None], [-10, None, -10], [10, None, 10],
           [None, -10, 10], [None, 10, -10]]
    data = np.array(raw, dtype=float)
    ids = [f"O{i + 1:02d}" for i in range(len(raw))]
    pairwise = np.eye(3)
    memberships = []
    for i, j in itertools.combinations(range(3), 2):
        keep = np.isfinite(data[:, i]) & np.isfinite(data[:, j])
        value = float(np.corrcoef(data[keep, i], data[keep, j])[0, 1])
        pairwise[i, j] = pairwise[j, i] = value
        memberships.append({"variables": [LABELS[i], LABELS[j]], "count": int(keep.sum()),
                            "observation_ids": [k for k, flag in zip(ids, keep) if flag], "correlation": value})
    complete_mask = np.isfinite(data).all(axis=1)
    complete = np.corrcoef(data[complete_mask], rowvar=False)
    matrices.update(pairwise_complete=pairwise, common_complete=complete)
    check("pairwise_correlations", pairwise, correlation(50 / 51, 50 / 51, -50 / 51))
    check("common_complete_correlations", complete, np.eye(3))
    check("pairwise_counts", [p["count"] for p in memberships], [6, 6, 6])
    check("common_count", complete_mask.sum(), 4)

    values, vectors = np.linalg.eigh(invalid)
    clipped_covariance = (vectors * np.maximum(values, 0)) @ vectors.T
    scales = np.sqrt(np.diag(clipped_covariance))
    clipped = clipped_covariance / np.outer(scales, scales)
    shrunk = 0.5 * invalid + 0.5 * np.eye(3)
    matrices.update(clipped_rescaled=clipped, shrunk_half=shrunk)
    check("clipped_rescaled_correlations", clipped, correlation(0.5, 0.5, -0.5))
    check("shrunk_correlations", shrunk, correlation(0.45, 0.45, -0.45))
    adjustments = {}
    for name in ["clipped_rescaled", "shrunk_half"]:
        matrix = matrices[name]
        delta = matrix - invalid
        adjustments[name] = {"delta": delta.tolist(), "maximum_absolute_change": float(np.max(np.abs(delta))),
                             "frobenius_change": float(np.linalg.norm(delta, "fro")),
                             "fixed_vector_quadratic_form": float(vector @ matrix @ vector),
                             "meets_illustrative_eigenvalue_floor": bool(np.linalg.eigvalsh(matrix)[0] >= 0.05 - TOL),
                             "preserves_locked_ab": bool(abs(matrix[0, 1] - 0.9) <= TOL)}
    check("clipped_spectrum", np.linalg.eigvalsh(clipped), [0, 1.5, 1.5])
    check("shrunk_spectrum", np.linalg.eigvalsh(shrunk), [0.1, 1.45, 1.45])

    aligned = correlation(0.6, 0.2, -0.1)
    exposures = np.array([1.0, 2.0, -1.0])
    permutation = [2, 0, 1]
    permuted = aligned[np.ix_(permutation, permutation)]
    bound_exposures = exposures[permutation]
    alignment = {"original_labels": LABELS, "permuted_labels": [LABELS[i] for i in permutation],
                 "original_matrix": aligned.tolist(), "permuted_matrix": permuted.tolist(),
                 "original_exposures": exposures.tolist(), "permuted_exposures": bound_exposures.tolist(),
                 "original_variance": float(exposures @ aligned @ exposures),
                 "correctly_bound_variance": float(bound_exposures @ permuted @ bound_exposures),
                 "positionally_misbound_variance": float(exposures @ permuted @ exposures)}
    check("original_variance", alignment["original_variance"], 8.4)
    check("aligned_variance", alignment["correctly_bound_variance"], 8.4)
    check("misbound_variance", alignment["positionally_misbound_variance"], 4.6)
    # Preserve actual variable labels separately; pair-block labels in inspect use the supplied order.
    matrices.update(alignment_original=aligned, alignment_permuted=permuted)
    inspected = {name: inspect(matrix) for name, matrix in matrices.items()}
    for name, entry in inspected.items():
        entry["variable_order"] = alignment["permuted_labels"] if name == "alignment_permuted" else LABELS
        for pair, (i, j) in zip(entry["pair_blocks"], itertools.combinations(range(3), 2)):
            pair["variables"] = [entry["variable_order"][i], entry["variable_order"][j]]
        check(f"eigen_reconstruction_{name}", entry["eigen_reconstruction_max_abs_error"], 0)

    return {"schema": "open-quant-dependence-observations-v1", "observed_at": datetime.now(timezone.utc).isoformat(),
            "environment": {"python": platform.python_version(), "numpy": np.__version__,
                            "platform": platform.platform(), "numpy_linalg_binary_sha256": sha(native_linalg.__file__)},
            "source_sha256": sha(__file__),
            "tolerance": TOL, "matrices": inspected,
            "negative_variance_witness": {"exposures": vector.tolist(), "quadratic_form": quadratic},
            "missing_data": {"variable_order": LABELS, "observations": [{"id": i, "values": r} for i, r in zip(ids, raw)],
                             "pairwise_membership": memberships,
                             "common_membership": [i for i, flag in zip(ids, complete_mask) if flag]},
            "adjustments": adjustments, "alignment": alignment, "checks": checks,
            "all_checks_passed": all(item["passed"] for item in checks.values()),
            "calculation_seconds": time.monotonic() - started}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = calculate()
    with args.output.open("x") as output:
        json.dump(result, output, indent=2, allow_nan=False)
        output.write("\n")
    print(json.dumps({"all_checks_passed": result["all_checks_passed"],
                      "checks": len(result["checks"]), "matrices": len(result["matrices"]),
                      "calculation_seconds": result["calculation_seconds"]}))
    raise SystemExit(0 if result["all_checks_passed"] else 1)
