"""One bounded native measurement; retain every prespecified case and control."""
from __future__ import annotations

import hashlib
import json
import math
import platform
import signal
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction as Q
from pathlib import Path

import numpy as np
import numpy.linalg._umath_linalg as native_linalg


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rational(value):
    return {"fraction": str(value), "decimal": float(value)}


def main():
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("120-second limit")))
    signal.alarm(120)
    output = Path(sys.argv[1])
    output.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).resolve()
    started = time.monotonic()
    data = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "platform": platform.platform(), "float": "binary64",
                        "linalg_binary_sha256": digest(native_linalg.__file__)},
        "identity": {"source_sha256": digest(source), "plan_sha256": digest(source.with_name("PLAN.md"))},
        "limits": {"processes": 1, "attempts": 1, "seconds": 120, "provider_calls": 0},
        "tolerances": {"parameter_absolute": 1e-10, "repricing_absolute": 1e-12,
                       "condition_relative": 1e-12},
        "spacings": [], "cases": [], "controls": [], "status": "running",
    }
    def save():
        data["elapsed_seconds"] = time.monotonic() - started
        (output / "observations.json").write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")

    def check(name, passed, **evidence):
        data["controls"].append({"name": name, "passed": bool(passed), **evidence})

    eta, a0, b0 = Q(1, 25000), Q(1, 25), Q(9, 100)
    offsets = [("baseline", 0, 0), ("common-up", 1, 1), ("common-down", -1, -1),
               ("steepen", -1, 1), ("flatten", 1, -1)]
    solve_calls = condition_calls = 0
    save()
    try:
        check("environment", platform.python_version() == "3.12.14" and np.__version__ == "2.5.3")
        for denominator in (1, 12, 365, 3650):
            eps = Q(1, denominator)
            original = np.array([[1., 0.], [1., float(eps)]], dtype=np.float64)
            integrated = np.array([[1., 0.], [1., 1.]], dtype=np.float64)
            lower, upper = b0 - 2 * eta / eps, b0 + 2 * eta / eps
            admissible_lower = max(Q(0), lower)
            spacing = {"epsilon": rational(eps), "eta": rational(eta),
                       "baseline_q": [rational(a0), rational(a0 + eps*b0)],
                       "raw_b_interval": [rational(lower), rational(upper)],
                       "admissible_b_interval": [rational(admissible_lower), rational(upper)],
                       "conditions": []}
            data["spacings"].append(spacing)
            for label, matrix, target in (("physical", original, 2*(1+eps)/eps),
                                           ("integrated", integrated, Q(4))):
                condition_calls += 1
                record = {"coordinates": label, "matrix": matrix.tolist(), "exact": rational(target)}
                spacing["conditions"].append(record)
                try:
                    value = float(np.linalg.cond(matrix, p=np.inf))
                    record.update(status="returned", value=value)
                    check(f"{eps}/{label}/condition", math.isclose(value, float(target), rel_tol=1e-12, abs_tol=0))
                except Exception as error:
                    record.update(status="error", error=repr(error))
                    check(f"{eps}/{label}/condition", False)
            points = [(name, a0+dx*eta, a0+eps*b0+dy*eta) for name, dx, dy in offsets]
            if denominator == 3650:
                points.append(("admissible-boundary", a0, a0))
            exact_bs = []
            admissible_bs = []
            for name, q1, q2 in points:
                identifier = f"{eps}/{name}"
                exact = [q1, (q2-q1)/eps]
                q_native = np.array([float(q1), float(q2)], dtype=np.float64)
                exact_bs.append(exact[1])
                admissible = all(value >= 0 for value in exact)
                if admissible:
                    admissible_bs.append(exact[1])
                case = {"id": identifier, "epsilon": str(eps), "name": name,
                        "intended_q": [rational(q1), rational(q2)], "native_q": q_native.tolist(),
                        "input_representation_error": [rational(Q.from_float(float(v))-q) for v,q in zip(q_native, (q1,q2))],
                        "exact_physical": [rational(v) for v in exact],
                        "variance_admissible_exact": admissible, "solves": []}
                data["cases"].append(case)
                check(identifier+"/input-box", abs(q1-a0) <= eta and abs(q2-(a0+eps*b0)) <= eta)
                check(identifier+"/exact-reprice", exact[0] == q1 and exact[0]+eps*exact[1] == q2)
                check(identifier+"/exact-b-range", lower <= exact[1] <= upper)
                if name.startswith("common"):
                    check(identifier+"/common-shift-b", exact[1] == b0)
                physical_results = []
                for coordinates, matrix in (("physical", original), ("integrated", integrated)):
                    solve_calls += 1
                    record = {"coordinates": coordinates}
                    case["solves"].append(record)
                    try:
                        solution = np.linalg.solve(matrix, q_native)
                        physical = [float(solution[0]), float(solution[1]) if coordinates == "physical" else float(solution[1])/float(eps)]
                        reprice = (original @ np.array(physical)).tolist()
                        residual = [v-float(q) for v,q in zip(reprice,q_native)]
                        errors = [v-float(target) for v,target in zip(physical,exact)]
                        record.update(status="returned", native_solution=solution.tolist(),
                                      physical_parameters=physical, repriced_q=reprice,
                                      residual=residual, parameter_error=errors,
                                      variance_admissible_native=all(v >= 0 for v in physical))
                        physical_results.append(physical)
                        check(identifier+"/"+coordinates+"/parameter", max(map(abs,errors)) <= 1e-10)
                        check(identifier+"/"+coordinates+"/repricing", max(map(abs,residual)) <= 1e-12)
                        check(identifier+"/"+coordinates+"/admissibility", record["variance_admissible_native"] == admissible)
                    except Exception as error:
                        record.update(status="error", error=repr(error))
                        check(identifier+"/"+coordinates+"/returned", False)
                check(identifier+"/coordinate-agreement", len(physical_results) == 2 and
                      max(abs(x-y) for x,y in zip(*physical_results)) <= 1e-10)
                save()
            check(f"{eps}/raw-extrema-witnesses", min(exact_bs) == lower and max(exact_bs) == upper)
            check(f"{eps}/admissible-extrema-witnesses", min(admissible_bs) == admissible_lower and max(admissible_bs) == upper)
        check("case-count", len(data["cases"]) == 21)
        check("solve-count", solve_calls == 42)
        check("condition-count", condition_calls == 8)
        check("inadmissible-count", sum(not row["variance_admissible_exact"] for row in data["cases"]) == 1)
        data["counts"] = {"cases": len(data["cases"]), "solve_calls": solve_calls,
                          "condition_calls": condition_calls, "controls": len(data["controls"]),
                          "passed": sum(row["passed"] for row in data["controls"])}
        data["status"] = "complete"
    except BaseException as error:
        data.update(status="error", error=repr(error), counts={"solve_calls": solve_calls, "condition_calls": condition_calls})
        raise
    finally:
        signal.alarm(0)
        save()
    print(json.dumps({"status": data["status"], "counts": data["counts"], "elapsed_seconds": data["elapsed_seconds"]}))
    return 0 if all(row["passed"] for row in data["controls"]) else 1


if __name__ == "__main__":
    sys.exit(main())
