"""Independent fixed-record arithmetic checks; does not run or import measure.py."""
import copy
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "examples/pricing-probabilities"


def equal(actual, expected):
    assert isinstance(actual, (float, int)) and not isinstance(actual, bool)
    assert math.isfinite(actual) and abs(F(str(actual)) - F(expected)) <= F(1, 10**10)


def verify(d):
    assert d["schema"] == "pricing-probabilities-study-v1"
    for key, filename in [("source_sha256", "model/measure.py"), ("plan_sha256", "model/README.md")]:
        assert d[key] == hashlib.sha256((ROOT / filename).read_bytes()).hexdigest()
    market = d["market"]
    assert market["state_order"] == ["down", "up"] and market["currency"] == "USD"
    assert market["horizon_years"] == 1 and market["exact_bond_price"] == "20/21"
    equal(market["bond_price"], F(20, 21)); equal(market["stock_price"], 100)
    assert market["terminal_stock_prices"] == [80, 130]
    z, q, D = F(10, 21), F(1, 2), F(20, 21)
    assert d["pricing"]["exact_state_prices"] == [str(z)] * 2
    assert d["pricing"]["exact_q_down_up"] == [str(q)] * 2
    for v in d["pricing"]["native_state_prices"]: equal(v, z)
    for v in d["pricing"]["native_q_down_up"]: equal(v, q)
    assert len(d["pricing"]["native_state_prices"]) == len(d["pricing"]["native_q_down_up"]) == 2
    # Hand-derived holdings, independent of the native solve and closed-form source inverse.
    cases = {"bond": ([1, 1], [F(1), F(0)]), "stock": ([80, 130], [F(0), F(1)]),
             "call-100": ([0, 30], [F(-48), F(3, 5)]), "put-100": ([20, 0], [F(52), F(-2, 5)]),
             "digital-up": ([0, 1], [F(-8, 5), F(1, 50)]), "digital-down": ([1, 0], [F(13, 5), F(-1, 50)])}
    assert [row["id"] for row in d["payoffs"]] == list(cases)
    for row in d["payoffs"]:
        payoff, holding = cases[row["id"]]
        assert row["payoff_down_up_usd"] == payoff
        price, mean = z * sum(payoff), q * sum(payoff)
        n, e = row["native"], row["exact"]
        assert e == {"price_usd": str(price), "bond_units_stock_shares": list(map(str, holding)), "q_expected_payoff_usd": str(mean)}
        equal(n["price_usd"], price); equal(n["replication_cost_usd"], price)
        equal(n["q_expected_payoff_usd"], mean)
        assert len(n["bond_units_stock_shares"]) == len(n["replicated_payoff_down_up_usd"]) == 2
        for actual, expected in zip(n["bond_units_stock_shares"], holding): equal(actual, expected)
        for index, state in enumerate([80, 130]):
            assert holding[0] + state * holding[1] == payoff[index]
            equal(n["replicated_payoff_down_up_usd"][index], payoff[index])
        assert D * holding[0] + 100 * holding[1] == price
    assert [w["id"] for w in d["physical_worlds"]] == ["A", "B"]
    for world, up in zip(d["physical_worlds"], [F(3, 5), F(4, 5)]):
        if d["case"] == "missing-world" and world["id"] == "B":
            assert world == dict(id="B", p_down_up=None, discount_factors_down_up=None, exact_p_down_up=None, exact_discount_factors_down_up=None, stock_expected_return=None, payoffs=None)
            continue
        p = [1 - up, up]; m = [z / v for v in p]
        assert world["exact_p_down_up"] == list(map(str, p))
        assert world["exact_discount_factors_down_up"] == list(map(str, m))
        assert len(world["p_down_up"]) == len(world["discount_factors_down_up"]) == 2
        for i in range(2):
            equal(world["p_down_up"][i], p[i]); equal(world["discount_factors_down_up"][i], m[i])
            assert p[i] > 0 and m[i] > 0 and p[i] * m[i] == z
        equal(world["stock_expected_return"], ((1-up)*80+up*130)/100-1)
        assert [r["id"] for r in world["payoffs"]] == list(cases)
        for row in world["payoffs"]:
            payoff = cases[row["id"]][0]
            mean = p[0]*payoff[0] + p[1]*payoff[1]
            equal(row["p_expected_payoff_usd"], mean)
            equal(row["p_expected_discounted_payoff_usd"], z*sum(payoff))
            assert row["exact_p_expected_payoff_usd"] == str(mean)
    assert d["equality_control"] == {"p_equals_q": ["1/2", "1/2"], "constant_discount_factor": "20/21"}
    assert d["case"] in ["complete", "missing-world", "contradictory"]
    claims = d["producer_statements"]
    assert [c["id"] for c in claims] == ([f"C{i}" for i in range(1, 8)] if d["case"] == "contradictory" else [])
    return {"pricing": "supported in the synthetic market", "A_physical_quantities": "supported under stipulated assumptions", "B_physical_quantities": "unresolved" if d["case"] == "missing-world" else "supported under stipulated assumptions", "empirical_forecast": "not established"}


def replace(d, path, value):
    for key in path[:-1]: d = d[key]
    d[path[-1]] = value


def main():
    packets = {case: json.loads((ROOT / "inputs" / (case + ".json")).read_text()) for case in ["complete", "missing-world", "contradictory"]}
    states = {case: verify(d) for case, d in packets.items()}
    receipt = json.loads((ROOT / "receipt.json").read_text())
    assert receipt["exit_code"] == 0 and receipt["model_calls"] == 0 and receipt["controls_passed"] == 63
    for case in packets:
        assert receipt["case_sha256"][case] == hashlib.sha256((ROOT / "inputs" / (case + ".json")).read_bytes()).hexdigest()
    assert receipt["source_sha256"] == packets["complete"]["source_sha256"]
    assert receipt["plan_sha256"] == packets["complete"]["plan_sha256"]
    d = packets["complete"]
    mutations = [
        ("state order", ["market", "state_order"], ["up", "down"]),
        ("horizon", ["market", "horizon_years"], 2),
        ("currency", ["market", "currency"], "EUR"),
        ("bond price", ["market", "bond_price"], 1),
        ("state price as probability", ["pricing", "native_q_down_up", 0], 10/21),
        ("probability as state price", ["pricing", "native_state_prices", 0], .5),
        ("changed payoff", ["payoffs", 2, "payoff_down_up_usd", 1], 31),
        ("missing discount", ["payoffs", 2, "native", "price_usd"], 15),
        ("wrong replication sign", ["payoffs", 3, "native", "bond_units_stock_shares", 1], .4),
        ("one state only", ["payoffs", 3, "native", "replicated_payoff_down_up_usd"], [20]),
        ("Q substituted for P", ["physical_worlds", 0, "p_down_up"], [.5, .5]),
        ("constant discount substituted", ["physical_worlds", 0, "discount_factors_down_up"], [20/21, 20/21]),
        ("world swap", ["physical_worlds", 1, "p_down_up"], [.4, .6]),
        ("discounted price called physical mean", ["physical_worlds", 0, "payoffs", 3, "p_expected_payoff_usd"], 200/21),
        ("Q mean called physical mean", ["physical_worlds", 0, "payoffs", 3, "p_expected_payoff_usd"], 10),
        ("discounted physical mean called price", ["physical_worlds", 0, "payoffs", 3, "p_expected_discounted_payoff_usd"], 160/21),
        ("percentage units", ["physical_worlds", 0, "stock_expected_return"], 10),
        ("nonfinite", ["payoffs", 0, "native", "price_usd"], float("nan")),
        ("lost source identity", ["source_sha256"], "0" * 64),
        ("duplicate payoff", ["payoffs", 5, "id"], "digital-up"),
    ]
    rejected = []
    for name, path, value in mutations:
        altered = copy.deepcopy(d); replace(altered, path, value)
        try: verify(altered)
        except (AssertionError, KeyError, TypeError, ValueError): rejected.append(name)
        else: raise AssertionError("Mutation accepted: " + name)
    for key in ["p_down_up", "discount_factors_down_up", "exact_p_down_up", "exact_discount_factors_down_up", "stock_expected_return", "payoffs"]:
        altered = copy.deepcopy(packets["missing-world"])
        altered["physical_worlds"][1][key] = packets["complete"]["physical_worlds"][1][key]
        try: verify(altered)
        except (AssertionError, KeyError, TypeError, ValueError): rejected.append("missing-world restores " + key)
        else: raise AssertionError("Missing projection accepted partial restoration")
    expected = copy.deepcopy(packets["complete"]); expected["case"] = "missing-world"
    expected["physical_worlds"][1] = dict(id="B", p_down_up=None, discount_factors_down_up=None, exact_p_down_up=None, exact_discount_factors_down_up=None, stock_expected_return=None, payoffs=None)
    assert expected == packets["missing-world"]
    contradiction = copy.deepcopy(packets["contradictory"]); contradiction["case"] = "complete"; contradiction["producer_statements"] = []
    assert contradiction == packets["complete"]
    # Check the authored report table and computed source locators, not arbitrary prose.
    report = (ROOT / "sample-results/report.md").read_text()
    rows = {}
    for line in report.splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells[0] in [r["id"] for r in d["payoffs"]]: rows[cells[0]] = list(map(float, cells[1:]))
    assert len(rows) == 6
    for i, r in enumerate(d["payoffs"]):
        vals = [r["native"]["price_usd"], r["native"]["q_expected_payoff_usd"], *[w["payoffs"][i]["p_expected_payoff_usd"] for w in d["physical_worlds"]]]
        assert len(rows[r["id"]]) == 4 and all(abs(x-y) <= .0000005 for x,y in zip(rows[r["id"]],vals))
    import re
    identities = re.findall(r"^- `([^`]+)` — `([0-9a-f]{64})`$", report, re.M)
    assert len(identities) == 9
    repo = ROOT.parents[1]
    for filename, digest in identities:
        assert hashlib.sha256((repo / filename).read_bytes()).hexdigest() == digest
    print(json.dumps({"packets": len(packets), "payoffs_each": 6, "rejected_mutations": len(rejected), "table_cells": 24, "identity_locators": len(identities), "states": states, "scope": "Fixed evidence checks; no pricing solve, model call or arbitrary prose evaluation."}))


if __name__ == "__main__": main()
