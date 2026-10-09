#!/usr/bin/env python3
"""Bootstrap the USD SOFR OIS discount curve for one as-of date and run the
tests the model document reports: repricing, forward smoothness, locality
under a single-input bump, the PV sensitivity ladder of an off-node cash flow,
convention sensitivities and interpolation variants. Two interpolation
methods are built from the same instruments:

  A. log-linear on discount factors (Hagan & West 2008 section 4.4, the "raw"
     method), with QuantLib's PiecewiseLogLinearDiscount.
  B. monotone convex on forward rates, unameliorated, with the positivity
     collar (Hagan & West 2008 section 6), implemented from the paper in
     hagan_west.py and bootstrapped there by a simultaneous solve.

QuantLib defines the instruments (calendar, schedules, payment dates) for
both methods. Its own ConvexMonotone bootstrap is recorded as a variant: the
paper's setting (quadraticity 0, monotonicity 1) fails in its iterative
bootstrap on these instruments, and its default smoothed setting (0.3, 0.7)
is a different interpolation from the paper's.

Inputs (from derive_quotes.py): out/quotes.csv, out/sofr_fixing.json.
Usage:
    uv run --with QuantLib==1.43 --with scipy --with matplotlib python3 bootstrap.py
Writes: out/*.csv, out/results.md, out/results.json, out/fig_*.png, out/run_info.json
"""
from __future__ import annotations

import csv
import json
import math
import platform
from datetime import date
from pathlib import Path

import QuantLib as ql
import scipy

import hagan_west as hw

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"

AS_OF = ql.Date(18, 9, 2026)
CAL = ql.UnitedStates(ql.UnitedStates.SOFR)
DC = ql.Actual365Fixed()          # curve time axis
ACT360 = ql.Actual360()
PAYMENT_LAG = 2                   # business days from period end to payment
NOTIONAL = 100_000_000.0          # USD, for PV figures
OFF_NODE_YEARS = 4.5              # the off-node example: a cash flow between 4Y and 5Y
BUMP = 1e-4                       # 1 bp
BUMP_TENOR = "5Y"
QL_CM_DEFAULT = (0.3, 0.7)        # QuantLib ConvexMonotone defaults (quadraticity, monotonicity)
METHODS = ("A", "B")
LABEL = {"A": "A: log-linear on discount factors", "B": "B: monotone convex (Hagan-West)"}

# Chart tokens (light surface) from the dataviz reference palette.
C_A, C_B, C_INK, C_MUTED, C_GRID, C_AXIS, C_SURF = "#2a78d6", "#eb6834", "#0b0b0b", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"


def pydate(d: ql.Date) -> date:
    return date(d.year(), d.month(), d.dayOfMonth())


def T(d: ql.Date) -> float:
    return DC.yearFraction(AS_OF, d)


def load_inputs():
    quotes = []
    with open(OUT / "quotes.csv") as f:
        for r in csv.DictReader(f):
            if r["used_in_bootstrap"] == "True":
                quotes.append((r["tenor"], float(r["quote_pct"]) / 100.0))
    fixing = json.loads((OUT / "sofr_fixing.json").read_text())
    return quotes, fixing["sofr_percent"] / 100.0


def ql_helpers(quotes, on_rate, bump_tenor=None, bump=0.0, payment_lag=PAYMENT_LAG, frequency=ql.Annual, tn_rate=None):
    """Overnight (as-of to next business day) and tom-next (to spot) deposits at
    the last known fixing, then one OIS per quoted tenor starting at spot."""
    helpers = [
        ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(rate)), ql.Period(1, ql.Days), fixing, CAL,
                             ql.Following, False, ACT360)
        for fixing, rate in ((0, on_rate), (1, on_rate if tn_rate is None else tn_rate))
    ]
    for tenor, rate in quotes:
        r = rate + (bump if tenor == bump_tenor else 0.0)
        helpers.append(ql.OISRateHelper(2, ql.Period(tenor), ql.QuoteHandle(ql.SimpleQuote(r)), ql.Sofr(),
                                        ql.YieldTermStructureHandle(), False, payment_lag, ql.Following,
                                        frequency, CAL))
    return helpers


def hw_instruments(helpers, names):
    """The same instruments as plain data for hagan_west.py: dates from QuantLib, pricing independent."""
    deposits, swaps = [], []
    for h, name in zip(helpers, names):
        if name in ("O/N", "T/N"):
            s, e = h.earliestDate(), h.maturityDate()
            deposits.append(hw.Deposit(name, T(s), T(e), ACT360.yearFraction(s, e), h.quote().value()))
        else:
            cps = [ql.as_fixed_rate_coupon(c) for c in h.swap().fixedLeg()]
            swaps.append(hw.Ois(name,
                                tuple(T(c.accrualStartDate()) for c in cps), tuple(T(c.accrualEndDate()) for c in cps),
                                tuple(T(c.date()) for c in cps), tuple(c.accrualPeriod() for c in cps),
                                h.quote().value(), T(h.pillarDate())))
    return deposits, swaps


class CurveSet:
    """Both curves from one instrument set."""

    def __init__(self, quotes, on_rate, bump_tenor=None, bump=0.0, payment_lag=PAYMENT_LAG, frequency=ql.Annual,
                 positive=True, tn_rate=None):
        self.quotes = quotes
        self.names = ["O/N", "T/N"] + [t for t, _ in quotes]
        self.helpers = ql_helpers(quotes, on_rate, bump_tenor, bump, payment_lag, frequency, tn_rate)
        self.ql_curve = ql.PiecewiseLogLinearDiscount(AS_OF, self.helpers, DC)
        self.ql_curve.enableExtrapolation()
        self.ql_curve.discount(1.0)  # build now, so each helper's implied quote refers to this curve
        self.deposits, self.swaps = hw_instruments(self.helpers, self.names)
        self.hw_curve = hw.bootstrap(self.deposits, self.swaps, "monotone_convex", positive=positive)
        self.pillars = [h.pillarDate() for h in self.helpers]

    def df(self, key, d):
        return self.ql_curve.discount(d) if key == "A" else self.hw_curve.discount(T(d))

    def zero(self, key, d):
        return -math.log(self.df(key, d)) / T(d)

    def on_forward(self, key, d):
        d2 = CAL.advance(d, 1, ql.Days)
        return (self.df(key, d) / self.df(key, d2) - 1.0) / ACT360.yearFraction(d, d2)

    def repricing(self, key):
        """(instrument, market, implied, error bp). A: QuantLib's implied quotes. B: the independent pricer."""
        rows = []
        for h, name in zip(self.helpers, self.names):
            mkt = h.quote().value()
            if key == "A":
                imp = h.impliedQuote()
            elif name in ("O/N", "T/N"):
                dep = next(x for x in self.deposits if x.name == name)
                imp = (self.hw_curve.discount(dep.start) / self.hw_curve.discount(dep.end) - 1.0) / dep.accrual
            else:
                imp = hw.ois_par_rate(self.hw_curve, next(x for x in self.swaps if x.name == name))
            rows.append((name, mkt, imp, (imp - mkt) * 1e4))
        return rows


def business_days(start, end):
    d, out = start, []
    while d <= end:
        out.append(d)
        d = CAL.advance(d, 1, ql.Days)
    return out


def main():
    OUT.mkdir(exist_ok=True)
    ql.Settings.instance().evaluationDate = AS_OF
    quotes, on_rate = load_inputs()
    base = CurveSet(quotes, on_rate)
    last_pillar = max(base.pillars)
    end31 = CAL.advance(last_pillar, 1, ql.Years)   # the daily grid runs through the last node and a year past it
    end40 = CAL.advance(AS_OF, 40, ql.Years)
    spot = CAL.advance(AS_OF, 2, ql.Days)

    # ---- nodes --------------------------------------------------------------
    with open(OUT / "nodes.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["instrument", "quote_pct", "pillar_date", "df_A", "df_B", "zero_A_pct", "zero_B_pct"])
        for h, name in zip(base.helpers, base.names):
            d = h.pillarDate()
            w.writerow([name, f"{100 * h.quote().value():.4f}", pydate(d).isoformat(),
                        f"{base.df('A', d):.8f}", f"{base.df('B', d):.8f}",
                        f"{100 * base.zero('A', d):.4f}", f"{100 * base.zero('B', d):.4f}"])

    # ---- 1. repricing --------------------------------------------------------
    rep = {k: base.repricing(k) for k in METHODS}
    max_err = {k: max(abs(r[3]) for r in rep[k]) for k in METHODS}
    with open(OUT / "repricing.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["instrument", "market_pct", "implied_A_pct", "error_A_bp", "implied_B_pct", "error_B_bp"])
        for ra, rb in zip(rep["A"], rep["B"]):
            w.writerow([ra[0], f"{100 * ra[1]:.6f}", f"{100 * ra[2]:.6f}", f"{ra[3]:.3e}", f"{100 * rb[2]:.6f}", f"{rb[3]:.3e}"])

    # ---- 2. grids ------------------------------------------------------------
    monthly = [CAL.advance(AS_OF, i, ql.Months) for i in range(0, 361)]
    diffs = []
    with open(OUT / "df_grid_monthly.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "years", "df_A", "df_B", "df_diff_A_minus_B", "zero_A_pct", "zero_B_pct"])
        for d in monthly:
            a, b = base.df("A", d), base.df("B", d)
            diffs.append((abs(a - b), d))
            za, zb = (100 * base.zero(k, d) if d > AS_OF else float("nan") for k in METHODS)
            w.writerow([pydate(d).isoformat(), f"{T(d):.4f}", f"{a:.8f}", f"{b:.8f}", f"{a - b:.3e}", f"{za:.4f}", f"{zb:.4f}"])
    max_df_diff, max_df_diff_date = max(diffs)

    days_all = business_days(AS_OF, end31)
    days = [d for d in days_all if d <= last_pillar]
    fwd_all = {k: [base.on_forward(k, d) for d in days_all] for k in METHODS}
    fwd = {k: v[: len(days)] for k, v in fwd_all.items()}
    with open(OUT / "forward_daily.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "years", "on_forward_A_pct", "on_forward_B_pct"])
        for d, a, b in zip(days_all, fwd_all["A"], fwd_all["B"]):
            w.writerow([pydate(d).isoformat(), f"{T(d):.4f}", f"{100 * a:.6f}", f"{100 * b:.6f}"])

    # ---- 3. forward smoothness and positivity ---------------------------------
    smooth = {}
    i_last = len(days) - 1
    for k in METHODS:
        jumps = [(abs(fwd[k][i] - fwd[k][i - 1]) * 1e4, days[i]) for i in range(1, i_last + 1)]
        jmax, jdate = max(jumps)
        smooth[k] = {
            "max_jump_bp": jmax, "max_jump_date": pydate(jdate).isoformat(),
            "jumps_over_2bp": sum(1 for j, _ in jumps if j > 2.0),
            "min_forward_pct": 100 * min(fwd[k]), "max_forward_pct": 100 * max(fwd[k]),
            "last_node_date": pydate(last_pillar).isoformat(),
            "jump_at_last_node_bp": abs(fwd_all[k][i_last + 1] - fwd_all[k][i_last]) * 1e4,
            "forward_last_node_pct": 100 * fwd_all[k][i_last],
            "forward_one_year_past_last_node_pct": 100 * fwd_all[k][-1],
        }
    # A grid-independent view of smoothness: the largest change of the forward
    # over any five consecutive business days (a short steep ramp is invisible
    # to a daily threshold), and the move just after the 3Y node.
    for k in METHODS:
        five = [(abs(fwd[k][i] - fwd[k][i - 5]) * 1e4, days[i]) for i in range(5, i_last + 1)]
        m5, d5 = max(five)
        smooth[k]["max_change_over_5_business_days_bp"] = m5
        smooth[k]["max_change_over_5_business_days_ending"] = pydate(d5).isoformat()
    i3 = days.index(dict(zip(base.names, base.pillars))["3Y"])
    after_3y = {k: {"forward_at_3Y_node_pct": 100 * fwd[k][i3], "forward_3_business_days_later_pct": 100 * fwd[k][i3 + 3],
                    "change_bp": (fwd[k][i3 + 3] - fwd[k][i3]) * 1e4} for k in METHODS}
    # Total variation of the daily forward, a single number for how much the curve wiggles.
    tv = {k: sum(abs(fwd[k][i] - fwd[k][i - 1]) for i in range(1, len(days))) * 1e4 for k in METHODS}

    # ---- 4. off-node example ------------------------------------------------
    off = CAL.advance(spot, int(OFF_NODE_YEARS * 12), ql.Months)
    off_df = {k: base.df(k, off) for k in METHODS}

    # ---- 5. locality: bump the 5Y quote by +1 bp ------------------------------
    bumped = CurveSet(quotes, on_rate, bump_tenor=BUMP_TENOR, bump=BUMP)
    node = dict(zip(base.names, base.pillars))
    d4, d6 = node["4Y"], node["6Y"]
    chg = {k: [(d, (bumped.on_forward(k, d) - base.on_forward(k, d)) * 1e4) for d in days] for k in METHODS}
    with open(OUT / "bump_5y_forward_change.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "years", "dfwd_A_bp", "dfwd_B_bp"])
        for (d, a), (_, b) in zip(chg["A"], chg["B"]):
            w.writerow([pydate(d).isoformat(), f"{T(d):.4f}", f"{a:.4f}", f"{b:.4f}"])
    locality = {}
    for k in METHODS:
        outside = [abs(c) for d, c in chg[k] if d < d4 or d > d6]
        locality[k] = {"max_change_inside_4Y_6Y_bp": max(abs(c) for d, c in chg[k] if d4 <= d <= d6),
                       "max_change_outside_4Y_6Y_bp": max(outside),
                       "first_date_with_change_over_0.01bp": next((pydate(d).isoformat() for d, c in chg[k] if abs(c) > 0.01), None),
                       "last_date_with_change_over_0.01bp": next((pydate(d).isoformat() for d, c in reversed(chg[k]) if abs(c) > 0.01), None)}

    # ---- 6. PV sensitivity ladder of one off-node cash flow ---------------------
    ladder = []
    for tenor, _ in quotes:
        bs = CurveSet(quotes, on_rate, bump_tenor=tenor, bump=BUMP)
        ladder.append((tenor, *[(bs.df(k, off) - off_df[k]) * NOTIONAL for k in METHODS]))
    with open(OUT / "delta_ladder_4p5y.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bumped_instrument", "pv_change_A_usd", "pv_change_B_usd"])
        for t, a, b in ladder:
            w.writerow([t, f"{a:.2f}", f"{b:.2f}"])
    leak = {}
    for i, k in enumerate(METHODS, start=1):
        total = sum(abs(r[i]) for r in ladder)
        local = sum(abs(r[i]) for r in ladder if r[0] in ("4Y", "5Y"))
        leak[k] = {"abs_pv_change_total_usd": total, "abs_pv_change_4Y_5Y_usd": local, "share_outside_4Y_5Y": 1 - local / total}

    # ---- 7. convention sensitivities and interpolation variants ----------------
    def variant_diff(df_fn, k):
        m = max(abs(df_fn(d) - base.df(k, d)) for d in monthly)
        return {"max_abs_df_diff_monthly_grid": m, "max_abs_pv_diff_per_notional_usd": m * NOTIONAL,
                "pv_diff_at_off_node_usd": (df_fn(off) - off_df[k]) * NOTIONAL}
    sens = {}
    lag0 = CurveSet(quotes, on_rate, payment_lag=0)
    sens["payment_lag_0_vs_2"] = {k: variant_diff(lambda d, k=k: lag0.df(k, d), k) for k in METHODS}
    qtr = CurveSet(quotes, on_rate, frequency=ql.Quarterly)
    sens["quarterly_vs_annual_payments"] = {k: variant_diff(lambda d, k=k: qtr.df(k, d), k) for k in METHODS}
    # Assumption checks: A004 read as Act/365 Fixed instead of Act/360 (the same
    # fixed cash flows then correspond to Act/360 rates scaled by 365/360), and
    # the overnight anchor 1 bp higher on both deposits.
    act365 = CurveSet([(t, r * 365.0 / 360.0) for t, r in quotes], on_rate)
    sens["fixed_leg_act365_vs_act360"] = {k: variant_diff(lambda d, k=k: act365.df(k, d), k) for k in METHODS}
    anchor = CurveSet(quotes, on_rate + BUMP)
    sens["anchor_plus_1bp"] = {k: variant_diff(lambda d, k=k: anchor.df(k, d), k) for k in METHODS}

    variants = {}
    nocollar = hw.bootstrap(base.deposits, base.swaps, "monotone_convex", positive=False)
    variants["B_without_positivity_collar"] = {"bootstrap": "converged", **variant_diff(lambda d: nocollar.discount(T(d)), "B")}
    for label, (qd, mo) in (("quantlib_convexmonotone_default_0.3_0.7", QL_CM_DEFAULT),
                            ("quantlib_convexmonotone_paper_setting_0_1", (0.0, 1.0))):
        try:
            c = ql.PiecewiseConvexMonotoneForward(AS_OF, ql_helpers(quotes, on_rate), DC, [], [], ql.ConvexMonotone(qd, mo, True))
            c.enableExtrapolation()
            c.discount(end40)
            v = {"bootstrap": "converged", **variant_diff(lambda d: c.discount(d), "B")}
            vf = [(c.forwardRate(d, CAL.advance(d, 1, ql.Days), ACT360, ql.Simple).rate()) for d in days_all]
            v["max_daily_forward_jump_bp"] = max(abs(vf[i] - vf[i - 1]) for i in range(1, len(days))) * 1e4
            v["jump_at_last_node_bp"] = abs(vf[i_last + 1] - vf[i_last]) * 1e4
            variants[label] = v
        except Exception as e:  # noqa: BLE001 - the failure message is the evidence
            variants[label] = {"bootstrap": "failed", "error": str(e).split("\n")[0][:240]}
    sectors = {}
    for i in range(1, base.hw_curve.n + 1):
        sectors[base.hw_curve.sector(i)] = sectors.get(base.hw_curve.sector(i), 0) + 1
    collar_binding = sum(1 for a, b in zip(base.hw_curve.f, nocollar.f) if abs(a - b) > 1e-12)

    # ---- 8. extrapolation past the last node ---------------------------------
    extrap = {k: {"df_40Y": base.df(k, end40), "zero_40Y_pct": 100 * base.zero(k, end40),
                  "on_forward_35Y_pct": 100 * base.on_forward(k, CAL.advance(AS_OF, 35, ql.Years))} for k in METHODS}

    # ---- figures -------------------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def style(ax, title, ylabel, xlabel="Years from as-of date (2026-09-18)"):
        ax.set_facecolor(C_SURF)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(C_AXIS)
        ax.tick_params(colors=C_MUTED, labelsize=9)
        ax.grid(True, color=C_GRID, linewidth=0.6)
        ax.set_title(title, color=C_INK, fontsize=11, loc="left")
        ax.set_ylabel(ylabel, color=C_MUTED, fontsize=9)
        ax.set_xlabel(xlabel, color=C_MUTED, fontsize=9)

    cap = f"Source: DTCC PPD CFTC cumulative rates 2026-09-18 (quotes), NY Fed SOFR (anchor); bootstrap.py, hagan_west.py, QuantLib {ql.__version__}"

    def figure(name, title, ylabel, xs, ya, yb, markers=None):
        fig, ax = plt.subplots(figsize=(9, 4.2), dpi=150, facecolor=C_SURF)
        style(ax, title, ylabel)
        ax.plot(xs, ya, color=C_A, linewidth=2, label=LABEL["A"])
        ax.plot(xs, yb, color=C_B, linewidth=2, label=LABEL["B"])
        if markers:
            ax.scatter(*markers, s=14, color=C_INK, zorder=3, label="Nodes")
        ax.legend(frameon=False, fontsize=9, labelcolor=C_INK)
        fig.text(0.01, 0.005, cap, color=C_MUTED, fontsize=7.5)
        fig.tight_layout(rect=(0, 0.03, 1, 1))
        fig.savefig(OUT / name, facecolor=C_SURF)
        plt.close(fig)

    yrs_m = [T(d) for d in monthly[1:]]
    figure("fig_discount_factors.png", "Discount factors, as-of 2026-09-18", "Discount factor", yrs_m,
           [base.df("A", d) for d in monthly[1:]], [base.df("B", d) for d in monthly[1:]])
    figure("fig_zero_rates.png", "Continuously compounded zero rates (Act/365F), as-of 2026-09-18", "Zero rate (%)", yrs_m,
           [100 * base.zero("A", d) for d in monthly[1:]], [100 * base.zero("B", d) for d in monthly[1:]],
           markers=([T(d) for d in base.pillars], [100 * base.zero("B", d) for d in base.pillars]))
    figure("fig_forwards.png", "Overnight forward rates (Act/360), as-of 2026-09-18, to one year past the 30Y node",
           "Overnight forward (%)", [T(d) for d in days_all], [100 * x for x in fwd_all["A"]], [100 * x for x in fwd_all["B"]])
    figure("fig_bump_5y.png", f"Change in overnight forwards when the {BUMP_TENOR} quote moves +1 bp", "Change (bp)",
           [T(d) for d in days], [c for _, c in chg["A"]], [c for _, c in chg["B"]])

    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=150, facecolor=C_SURF)
    style(ax, f"PV change of a USD {NOTIONAL / 1e6:.0f}m cash flow at {OFF_NODE_YEARS}Y per +1 bp on each input", "PV change (USD)",
          "Bumped instrument")
    xs = range(len(ladder))
    ax.bar([x - 0.2 for x in xs], [r[1] for r in ladder], width=0.4, color=C_A, label=LABEL["A"])
    ax.bar([x + 0.2 for x in xs], [r[2] for r in ladder], width=0.4, color=C_B, label=LABEL["B"])
    ax.set_xticks(list(xs))
    ax.set_xticklabels([r[0] for r in ladder], fontsize=8)
    ax.axhline(0, color=C_AXIS, linewidth=0.8)
    ax.legend(frameon=False, fontsize=9, labelcolor=C_INK)
    fig.text(0.01, 0.005, cap, color=C_MUTED, fontsize=7.5)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / "fig_delta_ladder.png", facecolor=C_SURF)
    plt.close(fig)

    # ---- results ---------------------------------------------------------------
    results = {
        "as_of": "2026-09-18", "spot": pydate(spot).isoformat(),
        "quantlib_version": ql.__version__, "scipy_version": scipy.__version__, "python": platform.python_version(),
        "instruments": base.names,
        "repricing_max_abs_error_bp": max_err,
        "df_difference_A_minus_B_monthly_grid": {"max_abs": max_df_diff, "max_abs_date": pydate(max_df_diff_date).isoformat(),
                                                  "max_abs_pv_per_notional_usd": max_df_diff * NOTIONAL},
        "forward_smoothness": smooth,
        "forward_total_variation_bp": tv,
        "off_node": {"date": pydate(off).isoformat(), "years": OFF_NODE_YEARS, "df": off_df,
                     "pv_of_notional_usd": {k: v * NOTIONAL for k, v in off_df.items()},
                     "pv_difference_A_minus_B_usd": (off_df["A"] - off_df["B"]) * NOTIONAL},
        "locality_bump_5Y_plus_1bp": locality,
        "pv_ladder_4p5y": leak,
        "extrapolation": extrap,
        "convention_sensitivities": sens,
        "interpolation_variants": variants,
        "hagan_west_sectors": sectors,
        "forward_after_3Y_node": after_3y,
        "discrete_forwards_pct": {
            "intervals": [f"{a}-{b}" for a, b in zip(["as-of"] + base.names[:-1], base.names)],
            "A": [100 * (math.log(base.df("A", d0) / base.df("A", d1)) / (T(d1) - T(d0))) for d0, d1 in zip([AS_OF] + base.pillars[:-1], base.pillars)],
            "B": [100 * x for x in base.hw_curve.fd]},
        "hagan_west_collar_binding_nodes": collar_binding,
        "notes": {
            "repricing": "A: QuantLib IterativeBootstrap default accuracy; B: simultaneous solve to 1e-14 in par rate. Errors measure solver tolerance, not model error.",
            "pv_ladder": "PV change of the cash flow per +1 bp on each input; not hedge notionals.",
        },
    }
    (OUT / "results.json").write_text(json.dumps(results, indent=2))

    def row(label, a, b=""):
        return f"| {label} | {a} | {b} |\n"
    with open(OUT / "results.md", "w") as f:
        f.write("Table: repricing of the input instruments, as-of 2026-09-18 (implied minus market, bp).\n\n")
        f.write("| Instrument | Market (%) | A implied (%) | A error (bp) | B implied (%) | B error (bp) |\n|---|---:|---:|---:|---:|---:|\n")
        for ra, rb in zip(rep["A"], rep["B"]):
            f.write(f"| {ra[0]} | {100 * ra[1]:.4f} | {100 * ra[2]:.4f} | {ra[3]:.1e} | {100 * rb[2]:.4f} | {rb[3]:.1e} |\n")
        f.write("\nSource: out/repricing.csv, bootstrap.py.\n\n")
        f.write("Table: curve nodes and discount factors.\n\n| Instrument | Quote (%) | Node date | DF (A) | DF (B) | Zero A (%) | Zero B (%) |\n|---|---:|---|---:|---:|---:|---:|\n")
        for h, name in zip(base.helpers, base.names):
            d = h.pillarDate()
            f.write(f"| {name} | {100 * h.quote().value():.4f} | {pydate(d).isoformat()} | {base.df('A', d):.8f} | {base.df('B', d):.8f} | {100 * base.zero('A', d):.4f} | {100 * base.zero('B', d):.4f} |\n")
        f.write("\nSource: out/nodes.csv, bootstrap.py.\n\n")
        f.write("Table: comparison metrics.\n\n| Metric | A: log-linear DF | B: monotone convex |\n|---|---:|---:|\n")
        f.write(row("Max abs repricing error (bp)", f"{max_err['A']:.1e}", f"{max_err['B']:.1e}"))
        f.write(row("Largest day-to-day jump in overnight forward, as-of date to last node (bp)",
                    f"{smooth['A']['max_jump_bp']:.2f} ({smooth['A']['max_jump_date']})", f"{smooth['B']['max_jump_bp']:.2f} ({smooth['B']['max_jump_date']})"))
        f.write(row("Day-to-day forward jumps over 2 bp (count)", smooth["A"]["jumps_over_2bp"], smooth["B"]["jumps_over_2bp"]))
        f.write(row("Total variation of the daily forward to the last node (bp)", f"{tv['A']:.1f}", f"{tv['B']:.1f}"))
        f.write(row("Largest change of the forward over 5 business days, to the last node (bp)",
                    f"{smooth['A']['max_change_over_5_business_days_bp']:.2f} ({smooth['A']['max_change_over_5_business_days_ending']})",
                    f"{smooth['B']['max_change_over_5_business_days_bp']:.2f} ({smooth['B']['max_change_over_5_business_days_ending']})"))
        f.write(row("Forward at the 3Y node and 3 business days later (%)",
                    f"{after_3y['A']['forward_at_3Y_node_pct']:.4f} / {after_3y['A']['forward_3_business_days_later_pct']:.4f}",
                    f"{after_3y['B']['forward_at_3Y_node_pct']:.4f} / {after_3y['B']['forward_3_business_days_later_pct']:.4f}"))
        i20 = days.index(node["20Y"])
        f.write(row("Average overnight forward (Act/360) over business days from the 20Y node to the day before the 30Y node (%)",
                    f"{100 * sum(fwd['A'][i20:i_last]) / (i_last - i20):.4f}", f"{100 * sum(fwd['B'][i20:i_last]) / (i_last - i20):.4f}"))
        f.write(row("Overnight forward (Act/360) at the 20Y node and at the 30Y node (%)",
                    f"{100 * fwd['A'][i20]:.4f} / {100 * fwd['A'][i_last]:.4f}", f"{100 * fwd['B'][i20]:.4f} / {100 * fwd['B'][i_last]:.4f}"))
        f.write(row("Min / max overnight forward to the last node (%)", f"{smooth['A']['min_forward_pct']:.4f} / {smooth['A']['max_forward_pct']:.4f}",
                    f"{smooth['B']['min_forward_pct']:.4f} / {smooth['B']['max_forward_pct']:.4f}"))
        f.write(row("Jump in overnight forward at the last node (bp)", f"{smooth['A']['jump_at_last_node_bp']:.2f}", f"{smooth['B']['jump_at_last_node_bp']:.2f}"))
        f.write(row(f"DF at {OFF_NODE_YEARS}Y ({pydate(off).isoformat()})", f"{off_df['A']:.8f}", f"{off_df['B']:.8f}"))
        f.write(row(f"PV of USD {NOTIONAL / 1e6:.0f}m at {OFF_NODE_YEARS}Y (USD)", f"{off_df['A'] * NOTIONAL:,.2f}", f"{off_df['B'] * NOTIONAL:,.2f}"))
        f.write(row(f"Max abs DF difference A-B on the monthly grid, and its date", f"{max_df_diff:.3e} ({pydate(max_df_diff_date).isoformat()})", "(one value for both)"))
        f.write(row(f"Same difference as PV of USD {NOTIONAL / 1e6:.0f}m paid on that date (USD)", f"{max_df_diff * NOTIONAL:,.2f}", "(one value for both)"))
        za, zb = (100 * base.zero(k, max_df_diff_date) for k in METHODS)
        f.write(row(f"Zero rate on that date (%)", f"{za:.4f}", f"{zb:.4f}"))
        f.write(row(f"Same difference as zero rate on that date, B minus A (bp)", f"{100 * (zb - za):.1f}", "(one value for both)"))
        f.write(row("5Y +1 bp: max forward change inside [4Y, 6Y] (bp)", f"{locality['A']['max_change_inside_4Y_6Y_bp']:.4f}", f"{locality['B']['max_change_inside_4Y_6Y_bp']:.4f}"))
        f.write(row("5Y +1 bp: max forward change outside [4Y, 6Y] (bp)", f"{locality['A']['max_change_outside_4Y_6Y_bp']:.4f}", f"{locality['B']['max_change_outside_4Y_6Y_bp']:.4f}"))
        f.write(row(f"{OFF_NODE_YEARS}Y cash flow: share of abs PV change outside the 4Y and 5Y inputs", f"{leak['A']['share_outside_4Y_5Y']:.2%}", f"{leak['B']['share_outside_4Y_5Y']:.2%}"))
        f.write(row("Payment lag 0 vs 2: max abs DF change (monthly grid)", f"{sens['payment_lag_0_vs_2']['A']['max_abs_df_diff_monthly_grid']:.2e}",
                    f"{sens['payment_lag_0_vs_2']['B']['max_abs_df_diff_monthly_grid']:.2e}"))
        f.write(row("Quarterly vs annual payments: max abs DF change (monthly grid)", f"{sens['quarterly_vs_annual_payments']['A']['max_abs_df_diff_monthly_grid']:.2e}",
                    f"{sens['quarterly_vs_annual_payments']['B']['max_abs_df_diff_monthly_grid']:.2e}"))
        f.write(row("Fixed leg read as Act/365 Fixed instead of Act/360: max abs DF change (monthly grid)", f"{sens['fixed_leg_act365_vs_act360']['A']['max_abs_df_diff_monthly_grid']:.2e}",
                    f"{sens['fixed_leg_act365_vs_act360']['B']['max_abs_df_diff_monthly_grid']:.2e}"))
        f.write(row("Overnight anchor +1 bp: max abs DF change (monthly grid)", f"{sens['anchor_plus_1bp']['A']['max_abs_df_diff_monthly_grid']:.2e}",
                    f"{sens['anchor_plus_1bp']['B']['max_abs_df_diff_monthly_grid']:.2e}"))
        f.write(row("Extrapolated DF at 40Y", f"{extrap['A']['df_40Y']:.8f}", f"{extrap['B']['df_40Y']:.8f}"))
        f.write(row("Extrapolated overnight forward at 35Y (%)", f"{extrap['A']['on_forward_35Y_pct']:.4f}", f"{extrap['B']['on_forward_35Y_pct']:.4f}"))
        f.write("\nSource: out/results.json, bootstrap.py.\n\n")
        f.write("Table: interpolation variants compared with method B.\n\n| Variant | Bootstrap | Max abs DF difference vs B (monthly grid) | Max daily forward jump (bp) | Jump at last node (bp) |\n|---|---|---:|---:|---:|\n")
        for label, v in variants.items():
            if v["bootstrap"] == "converged" and "max_daily_forward_jump_bp" not in v:
                f.write(f"| {label} | converged | {v['max_abs_df_diff_monthly_grid']:.2e} | as B | as B |\n")
            elif v["bootstrap"] == "converged":
                f.write(f"| {label} | converged | {v['max_abs_df_diff_monthly_grid']:.2e} | {v['max_daily_forward_jump_bp']:.2f} | {v['jump_at_last_node_bp']:.2f} |\n")
            else:
                f.write(f"| {label} | failed: {v['error']} | n/a | n/a | n/a |\n")
        f.write(f"\nHagan-West sectors used on the {base.hw_curve.n} intervals: "
                + ", ".join(f"{k}: {v}" for k, v in sorted(sectors.items())) + f". Positivity collar binding at {collar_binding} node(s).\n")
        f.write("\nSource: out/results.json, bootstrap.py, hagan_west.py.\n")

    (OUT / "run_info.json").write_text(json.dumps({"quantlib": ql.__version__, "scipy": scipy.__version__, "python": platform.python_version(),
                                                   "as_of": "2026-09-18", "scripts": ["derive_quotes.py", "bootstrap.py", "hagan_west.py"]}, indent=2))
    print((OUT / "results.md").read_text())


if __name__ == "__main__":
    main()
