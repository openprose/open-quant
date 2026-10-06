#!/usr/bin/env python3
"""Check fixed reference cells and identities; no native pricing or prose evaluation."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "examples/pricing-methodology"
SOURCE = ROOT / "examples/implementation-review"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(document, heading):
    section = document.split("## " + heading + "\n", 1)[1].split("\n## ", 1)[0]
    lines = [line for line in section.splitlines() if line.startswith("|")]
    return [[cell.strip() for cell in line.strip("|").split("|")] for line in lines[2:]]


packet = json.loads((SOURCE / "inputs/complete.json").read_text())
receipt = json.loads((SOURCE / "receipt.json").read_text())
assert digest(SOURCE / "model/measure.py") == packet["source_sha256"] == receipt["observer_sha256"]
assert digest(SOURCE / "inputs/complete.json") == receipt["projection"]["packets"]["complete"]["sha256"]
assert packet["absolute_tolerance"] == 1e-9
assert packet["price_units"] == "present-value USD per underlying unit"
observations = {row["case"]: row for row in packet["observations"]}
assert len(observations) == len(packet["observations"]) == 10
variants = {"A": "correct", "B": "wrong-time-scaling", "C": "omitted-discount"}
inputs = ("forward_usd", "strike_usd", "annual_volatility", "expiry_years", "continuous_rate")


def check(document):
    rows = table(document, "Retained numerical evidence")
    assert len(rows) == 10 and all(len(row) == 8 for row in rows), "price table population"
    assert len({row[0] for row in rows}) == 10 and {row[0] for row in rows} == set(observations), "case identities"
    for row in rows:
        actual = observations[row[0]]
        assert [float(cell) for cell in row[1:6]] == [actual["inputs"][key] for key in inputs], "input binding"
        for i, side in enumerate(("call", "put"), 6):
            expected = float(f'{actual["variants"]["correct"]["prices"][side]:.9f}')
            assert float(row[i]) == expected, "native price binding"
    summary = table(document, "Adapter differences and limits of simple checks")
    assert len(summary) == 3 and {row[0] for row in summary} == set(variants), "adapter population"
    assert all(len(row) == 6 for row in summary), "summary shape"
    for row in summary:
        variant = variants[row[0]]
        price_count, parity_count, errors = 0, 0, []
        for actual in observations.values():
            native = actual["variants"][variant]["prices"]
            refs = actual["reference"]
            assert all(not r["warnings"] and r["estimated_error"] >= 0 and r["tail_bound"] >= 0
                       and r["estimated_error"] + r["tail_bound"] <= 1e-9 for r in refs.values()), "reference criterion"
            diffs = [abs(native[side] - refs[side]["price"]) for side in ("call", "put")]
            price_count += all(value <= 1e-9 for value in diffs)
            parity_count += abs(native["call"] - native["put"] - actual["expected_parity"]) <= 1e-9
            errors.extend(diffs)
        assert [int(cell) for cell in row[3:5]] == [price_count, parity_count], "agreement counts"
        expected_max = float(f"{max(errors):.12g}" if row[0] == "A" else f"{max(errors):.9f}")
        assert float(row[5]) == expected_max, "maximum error binding"
    assert len(document.split()) < 1500, "reference word limit"
    assert document.count("[INSTITUTION-SUPPLIED:") == 3, "gap markers"


document = (BASE / "sample-results/document.md").read_text()
check(document)
mutations = [
    document.replace("| short-expiry | 100.0 | 100.0 | 0.2 | 0.25", "| short-expiry | 100.0 | 100.0 | 0.2 | 1.0"),
    document.replace("3.957964835 | 3.957964835", "7.965567455 | 3.957964835"),
    document.replace("23.384611746 | 4.549321074", "4.549321074 | 23.384611746"),
    document.replace("| short-expiry |", "| baseline |"),
    re.sub(r"^\| zero-strike \|.*\n", "", document, flags=re.M),
    document.replace("| 3 | 10 | 26.040808008 |", "| 10 | 10 | 26.040808008 |"),
    document.replace("1.42108547152e-14", "0"),
    document.replace("[INSTITUTION-SUPPLIED: accountable model owner and organization]", "Approved owner"),
]
for mutated in mutations:
    assert mutated != document, "mutation must change reference"
    try:
        check(mutated)
    except AssertionError:
        pass
    else:
        raise AssertionError("Mutation escaped fixed-reference controls")

reviews = (BASE / "sample-results/reviews.md").read_text()
ids = lambda text: re.findall(r"^\| (D\d+) \|", text, re.M)
assert ids((BASE / "requirements.md").read_text()) == ids(reviews) == [f"D{i}" for i in range(1, 9)]
result = (BASE / "sample-results/result.md").read_text()
identities = re.findall(r"^\| ([^|]+) \| ([a-f0-9]{64}) \|$", result, re.M)
assert len(identities) == len({path for path, _ in identities}) == 15
for path, recorded in identities:
    target = BASE / "sample-results" / path if path in {"document.md", "reviews.md"} else ROOT / path
    assert digest(target) == recorded, "source/artifact identity: " + path
print(json.dumps({"case_rows": 10, "input_cells": 50, "native_price_cells": 20,
                  "summary_numeric_cells": 9, "identities": 15, "mutations": len(mutations),
                  "scope": "Fixed reference cells, source identities and coverage markers; no financial run, arbitrary prose assessment or agent qualification."}, indent=2))
