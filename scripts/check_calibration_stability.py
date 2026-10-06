"""Check retained arithmetic and targeted corruptions without NumPy or a new solve."""
import copy
import hashlib
import json
import math
from fractions import Fraction as Q
from pathlib import Path


def verify(data):
    checked = 0
    def require(condition, message):
        nonlocal checked
        checked += 1
        if not condition:
            raise ValueError(message)
    def rational(record, expected):
        require(Q(record["fraction"]) == expected and record["decimal"] == float(expected), "rational identity")
    def close(actual, expected, tolerance=1e-10):
        require(math.isfinite(actual) and abs(actual-float(expected)) <= tolerance, "numeric identity")

    require(data["status"] == "complete", "incomplete record")
    require(len(data["spacings"]) == 4 and len(data["cases"]) == 21, "population")
    eta, a, b = Q(1,25000), Q(1,25), Q(9,100)
    expected_cases = []
    offsets = [("baseline",0,0),("common-up",1,1),("common-down",-1,-1),("steepen",-1,1),("flatten",1,-1)]
    for spacing, den in zip(data["spacings"], (1,12,365,3650)):
        eps = Q(1,den)
        rational(spacing["epsilon"], eps)
        rational(spacing["eta"], eta)
        for actual, expected in zip(spacing["baseline_q"], (a,a+eps*b)):
            rational(actual, expected)
        low, high = b-2*eta/eps, b+2*eta/eps
        for field, bounds in (("raw_b_interval", (low,high)), ("admissible_b_interval",(max(low,Q(0)),high))):
            require(len(spacing[field]) == 2, "bounds population")
            for actual, expected in zip(spacing[field],bounds):
                rational(actual,expected)
        require(len(spacing["conditions"]) == 2, "condition population")
        for record, name, coefficient in zip(spacing["conditions"],("physical","integrated"),(eps,Q(1))):
            # Exact row sums of A and its inverse, independent of the native condition call.
            matrix_norm = max(Q(1), 1+coefficient)
            inverse_norm = max(Q(1), 2/coefficient)
            target = matrix_norm*inverse_norm
            require(record["coordinates"] == name and record["status"] == "returned", "condition identity")
            require(record["matrix"] == [[1.,0.],[1.,float(coefficient)]], "condition matrix")
            rational(record["exact"],target)
            close(record["value"],target,float(target)*1e-12)
        expected_cases += [(eps,name,a+dx*eta,a+eps*b+dy*eta) for name,dx,dy in offsets]
        if den == 3650:
            expected_cases.append((eps,"admissible-boundary",a,a))
    for record,(eps,name,q1,q2) in zip(data["cases"],expected_cases):
        require(record["id"] == f"{eps}/{name}" and record["name"] == name and record["epsilon"] == str(eps), "case identity")
        physical = [q1,(q2-q1)/eps]
        native_q = [float(q1),float(q2)]
        require(record["native_q"] == native_q, "input rounding")
        require(abs(q1-a) <= eta and abs(q2-(a+eps*b)) <= eta, "input box")
        for field, expected in (("intended_q",[q1,q2]), ("exact_physical",physical),
                                 ("input_representation_error",[Q.from_float(v)-q for v,q in zip(native_q,(q1,q2))])):
            require(len(record[field]) == 2, "vector population")
            for actual,target in zip(record[field],expected):
                rational(actual,target)
        admissible = all(v >= 0 for v in physical)
        require(record["variance_admissible_exact"] == admissible, "exact admissibility")
        require(len(record["solves"]) == 2, "solve population")
        for solve, coordinates in zip(record["solves"],("physical","integrated")):
            require(solve["coordinates"] == coordinates and solve["status"] == "returned", "solve identity")
            native = solve["native_solution"]
            require(len(native) == 2 and len(solve["physical_parameters"]) == 2, "native parameter population")
            mapped = [native[0],native[1] if coordinates == "physical" else native[1]/float(eps)]
            for actual,target in zip(solve["physical_parameters"],mapped):
                close(actual,target,0)
            for actual,target,error in zip(mapped,physical,solve["parameter_error"]):
                close(actual,target)
                close(error,actual-float(target),0)
            repriced = [mapped[0], mapped[0]+float(eps)*mapped[1]]
            for actual,target,residual,q in zip(solve["repriced_q"],repriced,solve["residual"],native_q):
                close(actual,target,1e-15)
                close(residual,actual-q,0)
                close(actual,q,1e-12)
            require(solve["variance_admissible_native"] == all(v >= 0 for v in mapped) == admissible, "native admissibility")
    return checked


def main():
    folder = Path(__file__).resolve().parents[1] / "examples/calibration-stability"
    source = folder / "model/observations.json"
    data = json.loads(source.read_text())
    count = verify(data)
    receipt = json.loads((folder / "receipt.json").read_text())
    for entry in receipt["files"]:
        assert hashlib.sha256((folder / entry["path"]).read_bytes()).hexdigest() == entry["sha256"], entry["path"]
    assert data["identity"]["source_sha256"] == hashlib.sha256((folder / "model/measure.py").read_bytes()).hexdigest()
    assert data["identity"]["plan_sha256"] == hashlib.sha256((folder / "model/PLAN.md").read_bytes()).hexdigest()
    assert receipt["calculation_counts"] == data["counts"]
    expected = {"case":"complete", "spacings":[{"epsilon":s["epsilon"]["fraction"], "native_conditions":[{k:v for k,v in c.items() if k != "exact"} for c in s["conditions"]]} for s in data["spacings"]], "native_cases":[{k:copy.deepcopy(c[k]) for k in ("id","epsilon","name","native_q","solves")} for c in data["cases"]], "producer_claims":[]}
    for case in expected["native_cases"]:
        for solve in case["solves"]:
            solve.pop("parameter_error")
            solve.pop("variance_admissible_native")
    complete = json.loads((folder / "inputs/complete.json").read_text())
    assert complete == expected, "complete projection"
    missing = copy.deepcopy(expected)
    missing["case"] = "missing-perturbations"
    missing["native_cases"] = [row for row in missing["native_cases"] if row["name"] == "baseline"]
    assert json.loads((folder / "inputs/missing-perturbations.json").read_text()) == missing, "missing projection"
    contradictory = json.loads((folder / "inputs/contradictory.json").read_text())
    assert [x["id"] for x in contradictory["producer_claims"]] == ["C1","C2","C3","C4","C5"]
    contradictory["case"] = "complete"
    contradictory["producer_claims"] = []
    assert contradictory == complete, "contradictory records"
    report = (folder / "sample-results/report.md").read_text()
    for row in data["spacings"]:
        eps = Q(row["epsilon"]["fraction"])
        low, high = Q(9,100)-Q(2,25000)/eps, Q(9,100)+Q(2,25000)/eps
        physical = int(2*(1+eps)/eps)
        raw = f"[{float(low):g}, {float(high):g}]"
        admissible = f"[{float(max(Q(0),low)):g}, {float(high):g}]"
        assert f"| {eps} | {physical} | 4 | {raw} | {admissible} |" in report, "authored interval row"
    mutations = []
    def reject(label, mutate):
        changed = copy.deepcopy(data)
        mutate(changed)
        try:
            verify(changed)
        except (ValueError,KeyError,IndexError,TypeError):
            mutations.append({"name":label,"rejected":True})
        else:
            raise AssertionError("Undetected mutation: "+label)
    reject("omit-boundary",lambda x:x["cases"].pop())
    reject("duplicate-case",lambda x:x["cases"].__setitem__(-1,copy.deepcopy(x["cases"][-2])))
    reject("swap-condition-coordinates",lambda x:x["spacings"][-1]["conditions"].reverse())
    reject("claim-physical-condition-four",lambda x:x["spacings"][-1]["conditions"][0].__setitem__("value",4.))
    reject("narrow-physical-interval",lambda x:x["spacings"][-1].__setitem__("admissible_b_interval",copy.deepcopy(x["spacings"][0]["admissible_b_interval"])))
    reject("negative-rate-marked-valid",lambda x:x["cases"][-2].__setitem__("variance_admissible_exact",True))
    reject("omit-coordinate-mapping",lambda x:x["cases"][-3]["solves"][1].__setitem__("physical_parameters",x["cases"][-3]["solves"][1]["native_solution"]))
    reject("hide-residual",lambda x:x["cases"][0]["solves"][0]["residual"].__setitem__(0,.01))
    reject("changed-reprice",lambda x:x["cases"][0]["solves"][0]["repriced_q"].__setitem__(0,.05))
    reject("omit-solve",lambda x:x["cases"][0]["solves"].pop())
    reject("alter-input",lambda x:x["cases"][0]["native_q"].__setitem__(0,.05))
    reject("erase-rounding-error",lambda x:x["cases"][0]["input_representation_error"][0].__setitem__("fraction","0"))
    result={"source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
            "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "arithmetic_checks":count,"projection_checks":3,"authored_table_rows":4,"mutations":mutations,"native_calls":0,"provider_calls":0}
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
