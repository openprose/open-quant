#!/usr/bin/env python3
"""Reproduce the synthetic Black adapter comparison; no market data or model API is used."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import signal
import sys
import time
import warnings

import QuantLib as ql
import QuantLib._QuantLib as native
import scipy
from scipy.integrate import quad

TOLERANCE = 1e-9
VARIANTS = ("correct", "wrong-time-scaling", "omitted-discount")
CASES = [
    ("baseline", 100., 100., .2, 1., 0.),
    ("short-expiry", 100., 100., .2, .25, .03),
    ("long-expiry", 100., 100., .2, 4., .03),
    ("in-the-money", 120., 100., .2, 2., .03),
    ("out-of-the-money", 80., 100., .2, 2., .03),
    ("zero-volatility", 120., 100., 0., 2., .03),
    ("zero-expiry", 120., 100., .2, 0., .03),
    ("zero-strike", 100., 0., .2, 2., .03),
    ("negative-rate", 100., 100., .2, 2., -.01),
    ("higher-volatility", 100., 100., .8, 5., .04),
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def domain(f, k, sigma, expiry, rate):
    if not all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
               for x in (f, k, sigma, expiry, rate)):
        raise ValueError("finite numeric inputs required")
    if f <= 0 or k < 0 or sigma < 0 or expiry < 0:
        raise ValueError("outside selected positive-forward Black domain")


def price(variant, is_call, f, k, sigma, expiry, rate):
    domain(f, k, sigma, expiry, rate)
    std_dev = sigma if variant == "wrong-time-scaling" else sigma * math.sqrt(expiry)
    discount = 1. if variant == "omitted-discount" else math.exp(-rate * expiry)
    return ql.blackFormula(ql.Option.Call if is_call else ql.Option.Put, k, f, std_dev, discount, 0.)


def reference(is_call, f, k, sigma, expiry, rate):
    domain(f, k, sigma, expiry, rate)
    discount = math.exp(-rate * expiry)
    s = sigma * math.sqrt(expiry)
    sign = 1 if is_call else -1
    if s == 0:
        return {"price": discount * max(sign * (f - k), 0.), "estimated_error": 0.,
                "tail_bound": 0., "warnings": [], "method": "deterministic payoff"}
    def integrand(z):
        terminal = f * math.exp(-.5 * s * s + s * z)
        return discount * max(sign * (terminal - k), 0.) * math.exp(-.5 * z * z) / math.sqrt(2 * math.pi)
    cut = (math.log(k / f) + .5 * s * s) / s if k > 0 else -math.inf
    knots = [-12., *([cut] if -12 < cut < 12 else []), 12.]
    values, errors, warning_messages = [], [], []
    for a, b in zip(knots, knots[1:]):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            value, error = quad(integrand, a, b, epsabs=1e-11, epsrel=1e-11, limit=200)
        values.append(value)
        errors.append(error)
        warning_messages.extend(str(w.message) for w in caught)
    cdf = lambda x: .5 * math.erfc(-x / math.sqrt(2))
    tail = discount * (f * (cdf(-12 - s) + cdf(s - 12)) + 2 * k * cdf(-12))
    return {"price": math.fsum(values), "estimated_error": math.fsum(errors),
            "tail_bound": tail, "warnings": warning_messages, "method": "discounted payoff quadrature", "integration_knots": knots}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output already exists; require a fresh path")
    assert platform.python_version() == "3.12.14" and ql.__version__ == "1.43" and scipy.__version__ == "1.18.1"
    native_hash = sha(native.__file__)
    signal.alarm(120)
    start = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    observations = []
    for name, f, k, sigma, expiry, rate in CASES:
        refs = {side: reference(side == "call", f, k, sigma, expiry, rate) for side in ("call", "put")}
        usable = all(not r["warnings"] and r["estimated_error"] + r["tail_bound"] <= TOLERANCE for r in refs.values())
        expected_parity = math.exp(-rate * expiry) * (f - k)
        variants = {}
        for variant in VARIANTS:
            prices = {side: price(variant, side == "call", f, k, sigma, expiry, rate) for side in ("call", "put")}
            errors = {side: prices[side] - refs[side]["price"] for side in prices}
            parity_error = prices["call"] - prices["put"] - expected_parity
            variants[variant] = {"prices": prices, "price_errors": errors,
                                 "price_agreement": all(abs(e) <= TOLERANCE for e in errors.values()) if usable else None,
                                 "parity_error": parity_error, "parity_agreement": abs(parity_error) <= TOLERANCE}
        observations.append({"case": name, "inputs": {"forward_usd": f, "strike_usd": k, "annual_volatility": sigma, "expiry_years": expiry, "continuous_rate": rate},
                             "reference": refs, "reference_usable": usable, "expected_parity": expected_parity, "variants": variants})
    invalid = []
    for variant in VARIANTS:
        for name, inputs in [("zero-forward", (0., 100., .2, 1., .03)), ("negative-strike", (100., -1., .2, 1., .03)),
                             ("negative-volatility", (100., 100., -.2, 1., .03)), ("negative-expiry", (100., 100., .2, -1., .03))]:
            try:
                value = price(variant, True, *inputs)
                invalid.append({"variant": variant, "case": name, "inputs": inputs, "rejected": False, "value": value})
            except ValueError as exc:
                invalid.append({"variant": variant, "case": name, "inputs": inputs, "rejected": True, "error": str(exc)})
    summary = {variant: {"price_agreement_cases": sum(row["variants"][variant]["price_agreement"] is True for row in observations),
                         "parity_agreement_cases": sum(row["variants"][variant]["parity_agreement"] for row in observations),
                         "max_abs_price_error": max(abs(e) for row in observations for e in row["variants"][variant]["price_errors"].values())} for variant in VARIANTS}
    result = {"started_at": start, "ended_at": datetime.now(timezone.utc).isoformat(), "duration_seconds": time.monotonic() - clock,
              "timeout_seconds": 120, "provider_calls": 0, "command": sys.argv,
              "environment": {"python": platform.python_version(), "quantlib": ql.__version__, "scipy": scipy.__version__, "platform": platform.platform()},
              "native_extension_sha256": native_hash, "observer_sha256": sha(__file__),
              "price_units": "present-value USD per underlying unit", "absolute_tolerance": TOLERANCE,
              "observations": observations, "invalid_input_controls": invalid, "summary": summary}
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(summary))
    return int(not all(r["reference_usable"] and r["variants"]["correct"]["price_agreement"] and r["variants"]["correct"]["parity_agreement"] for r in observations)
               or not all(r["rejected"] for r in invalid))


if __name__ == "__main__":
    raise SystemExit(main())
