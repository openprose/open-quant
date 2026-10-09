"""One fixed two-state pricing calculation; emits observations to the supplied path."""
import hashlib
import json
import platform
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path

import numpy as np


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def exact_solve(a, b):
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [(b[0] * a[1][1] - a[0][1] * b[1]) / determinant,
            (a[0][0] * b[1] - b[0] * a[1][0]) / determinant]


def main(output):
    start = time.perf_counter()
    D, S0 = F(20, 21), F(100)
    stock = [F(80), F(130)]
    system = [[F(1), F(1)], stock]
    state_prices = exact_solve(system, [D, S0])
    q = [v / D for v in state_prices]
    native_state = np.linalg.solve(np.array(system, dtype=float), [float(D), float(S0)])
    native_q = native_state / float(D)
    payoffs = {"bond": [1, 1], "stock": [80, 130], "call-100": [0, 30],
               "put-100": [20, 0], "digital-up": [0, 1], "digital-down": [1, 0]}
    replication_system = [[F(1), stock[0]], [F(1), stock[1]]]
    controls = []

    def check(name, value, target=0, unit="dimensionless"):
        error = abs(float(value) - float(target))
        controls.append({"id": name, "value": float(value), "reference": float(target),
                         "absolute_error": error, "unit": unit, "passed": error <= 1e-10})

    check("state-price-down", native_state[0], state_prices[0], "USD per USD payoff")
    check("state-price-up", native_state[1], state_prices[1], "USD per USD payoff")
    check("state-price-sum", sum(native_state), D, "USD per USD payoff")
    check("risk-neutral-sum", sum(native_q), 1)
    check("risk-neutral-stock-growth", native_q @ np.array(stock, dtype=float), S0 / D, "USD/share")
    rows = []
    for name, values in payoffs.items():
        payoff = list(map(F, values))
        holdings = exact_solve(replication_system, payoff)
        native_holdings = np.linalg.solve(np.array(replication_system, dtype=float), values)
        price = dot(state_prices, payoff)
        native_price = float(native_state @ np.array(values))
        native_rep_price = float(np.array([float(D), float(S0)]) @ native_holdings)
        native_payoff = np.array(replication_system, dtype=float) @ native_holdings
        eq = dot(q, payoff)
        for s in range(2):
            check(f"{name}:replication-state-{s}", native_payoff[s], payoff[s], "USD at T")
        check(f"{name}:price", native_price, price, "USD at t=0")
        check(f"{name}:replication-cost", native_rep_price, price, "USD at t=0")
        check(f"{name}:discounted-Q", float(D) * float(native_q @ np.array(values)), price, "USD at t=0")
        rows.append({"id": name, "payoff_down_up_usd": values,
                     "native": {"price_usd": native_price, "replication_cost_usd": native_rep_price,
                                "bond_units_stock_shares": native_holdings.tolist(),
                                "replicated_payoff_down_up_usd": native_payoff.tolist(),
                                "q_expected_payoff_usd": float(native_q @ np.array(values))},
                     "exact": {"price_usd": str(price), "bond_units_stock_shares": list(map(str, holdings)),
                               "q_expected_payoff_usd": str(eq)}})
    worlds = []
    for name, p_up in [("A", F(3, 5)), ("B", F(4, 5))]:
        p = [1 - p_up, p_up]
        m = [z / probability for z, probability in zip(state_prices, p)]
        native_p = np.array(p, dtype=float)
        native_m = native_state / native_p
        records = []
        for name_payoff, values in payoffs.items():
            physical_mean = dot(p, list(map(F, values)))
            discounted = float((native_p * native_m) @ np.array(values))
            mean = float(native_p @ np.array(values))
            check(f"world-{name}:{name_payoff}:price", discounted, dot(state_prices, list(map(F, values))), "USD at t=0")
            check(f"world-{name}:{name_payoff}:mean", mean, physical_mean, "USD at T")
            records.append({"id": name_payoff, "p_expected_payoff_usd": mean,
                            "p_expected_discounted_payoff_usd": discounted,
                            "exact_p_expected_payoff_usd": str(physical_mean)})
        check(f"world-{name}:expected-discount", native_p @ native_m, D)
        worlds.append({"id": name, "p_down_up": list(map(float, p)),
                       "discount_factors_down_up": native_m.tolist(),
                       "exact_p_down_up": list(map(str, p)),
                       "exact_discount_factors_down_up": list(map(str, m)),
                       "stock_expected_return": float(dot(p, stock) / S0 - 1), "payoffs": records})
    equality_m = [z / probability for z, probability in zip(state_prices, q)]
    check("P-equals-Q:constant-discount-down", equality_m[0], D)
    check("P-equals-Q:constant-discount-up", equality_m[1], D)
    result = {"schema": "pricing-probabilities-study-v1", "recorded_at": datetime.now(timezone.utc).isoformat(),
              "source_sha256": sha(Path(__file__)), "plan_sha256": sha(Path(__file__).with_name("README.md")),
              "environment": {"python": platform.python_version(), "numpy": np.__version__, "platform": platform.platform()},
              "market": {"currency": "USD", "horizon_years": 1, "state_order": ["down", "up"],
                         "bond_price": float(D), "exact_bond_price": str(D), "stock_price": float(S0),
                         "terminal_stock_prices": list(map(float, stock))},
              "pricing": {"native_state_prices": native_state.tolist(), "exact_state_prices": list(map(str, state_prices)),
                          "native_q_down_up": native_q.tolist(), "exact_q_down_up": list(map(str, q))},
              "payoffs": rows, "physical_worlds": worlds,
              "equality_control": {"p_equals_q": list(map(str, q)), "constant_discount_factor": str(D)},
              "controls": controls, "calculation_seconds": time.perf_counter() - start}
    output = Path(output)
    with output.open("x") as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write("\n")
    print(json.dumps({"output": str(output), "controls": len(controls), "passed": sum(c["passed"] for c in controls)}))
    if not all(c["passed"] for c in controls):
        raise SystemExit(1)


if __name__ == "__main__":
    main(sys.argv[1])
