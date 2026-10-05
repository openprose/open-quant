#!/usr/bin/env python3
"""Hagan-West monotone convex interpolation and an OIS bootstrap built on it,
implemented from the paper and independent of QuantLib's curve classes.

Source: Hagan, P. S. and West, G., "Methods for Constructing a Yield Curve",
Wilmott Magazine, May 2008, section 6 (printed pp. 75-77): equations (22)-(24)
for the instantaneous forwards at the nodes, (25)-(27) for the normalised
function g on each interval, the four sectors (i)-(iv) with equations
(28)-(34), and the positivity collar of section 6.1, step (3). This is the
unameliorated method, which p. 79 recommends.

Conventions of this module:
  * times are year fractions from the as-of date (Act/365F), t_0 = 0;
  * the inputs of the interpolation are discrete forwards fd_i, one for each
    interval (t_{i-1}, t_i]; the discount factor at node t_i is
    exp(-sum_{j<=i} fd_j (t_j - t_{j-1})), so every node is recovered exactly
    (condition (i) of the paper);
  * past the last node the instantaneous forward is held at f_n, its value at
    the last node, so the forward curve is continuous there.

The bootstrap solves for the discrete forwards of the OIS intervals so that
every instrument reprices at its par rate, all at once (a square nonlinear
system solved by scipy's hybrid Powell method). A node-by-node bootstrap is
not used because the interpolation on an interval depends on its neighbours.
"""
from __future__ import annotations

import bisect
import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import root


class MonotoneConvex:
    """Instantaneous forward curve on [0, t_n] from discrete forwards."""

    def __init__(self, t: list[float], fd: list[float], positive: bool = True):
        t = [float(x) for x in t]
        fd = [float(x) for x in fd]
        n = len(fd)
        if len(t) != n + 1 or t[0] != 0.0 or any(b <= a for a, b in zip(t, t[1:])):
            raise ValueError("need increasing node times starting at 0 and one discrete forward per interval")
        self.t, self.fd, self.n = t, fd, n
        f = [0.0] * (n + 1)
        if n == 1:
            f[0] = f[1] = fd[0]
        else:
            for i in range(1, n):  # eq. (22); fd_i is fd[i-1] and fd_{i+1} is fd[i]
                f[i] = ((t[i] - t[i - 1]) * fd[i] + (t[i + 1] - t[i]) * fd[i - 1]) / (t[i + 1] - t[i - 1])
            f[0] = fd[0] - 0.5 * (f[1] - fd[0])            # eq. (23)
            f[n] = fd[n - 1] - 0.5 * (f[n - 1] - fd[n - 1])  # eq. (24)
        if positive:  # section 6.1, step (3)
            f[0] = _collar(0.0, f[0], 2.0 * fd[0])
            for i in range(1, n):
                f[i] = _collar(0.0, f[i], 2.0 * min(fd[i - 1], fd[i]))
            f[n] = _collar(0.0, f[n], 2.0 * fd[n - 1])
        self.f = f
        self.cum = [0.0]
        for i in range(n):
            self.cum.append(self.cum[-1] + fd[i] * (t[i + 1] - t[i]))

    def _locate(self, s: float) -> int:
        """Index i of the interval (t_{i-1}, t_i] containing s, for 0 < s <= t_n."""
        return max(1, bisect.bisect_left(self.t, s))

    def forward(self, s: float) -> float:
        """Instantaneous forward f(s), eq. (26)."""
        if s >= self.t[-1]:
            return self.f[-1]
        if s <= 0.0:
            return self.f[0]
        i = self._locate(s)
        x = (s - self.t[i - 1]) / (self.t[i] - self.t[i - 1])
        g0, g1 = self.f[i - 1] - self.fd[i - 1], self.f[i] - self.fd[i - 1]
        return self.fd[i - 1] + _g(g0, g1, x)

    def integral(self, s: float) -> float:
        """Integral of f from 0 to s, so that the discount factor is exp(-integral)."""
        if s <= 0.0:
            return 0.0
        if s >= self.t[-1]:
            return self.cum[-1] + self.f[-1] * (s - self.t[-1])
        i = self._locate(s)
        h = self.t[i] - self.t[i - 1]
        x = (s - self.t[i - 1]) / h
        g0, g1 = self.f[i - 1] - self.fd[i - 1], self.f[i] - self.fd[i - 1]
        return self.cum[i - 1] + self.fd[i - 1] * (s - self.t[i - 1]) + h * _G(g0, g1, x)

    def discount(self, s: float) -> float:
        return math.exp(-self.integral(s))

    def sector(self, i: int) -> str:
        g0, g1 = self.f[i - 1] - self.fd[i - 1], self.f[i] - self.fd[i - 1]
        return _sector(g0, g1)


class LogLinearDiscount:
    """Piecewise-flat instantaneous forwards: log-linear interpolation on discount
    factors (Hagan and West 2008, section 4.4, the 'raw' method)."""

    def __init__(self, t: list[float], fd: list[float]):
        self.t, self.fd = [float(x) for x in t], [float(x) for x in fd]
        self.cum = [0.0]
        for i in range(len(self.fd)):
            self.cum.append(self.cum[-1] + self.fd[i] * (self.t[i + 1] - self.t[i]))

    def forward(self, s: float) -> float:
        if s >= self.t[-1]:
            return self.fd[-1]
        return self.fd[max(1, bisect.bisect_left(self.t, s)) - 1]

    def integral(self, s: float) -> float:
        if s <= 0.0:
            return 0.0
        if s >= self.t[-1]:
            return self.cum[-1] + self.fd[-1] * (s - self.t[-1])
        i = max(1, bisect.bisect_left(self.t, s))
        return self.cum[i - 1] + self.fd[i - 1] * (s - self.t[i - 1])

    def discount(self, s: float) -> float:
        return math.exp(-self.integral(s))


def _collar(lo: float, x: float, hi: float) -> float:
    return max(lo, min(x, hi))


def _sector(g0: float, g1: float) -> str:
    if g0 == 0.0 and g1 == 0.0:
        return "origin"
    if (g0 < 0 and -0.5 * g0 <= g1 <= -2.0 * g0) or (g0 > 0 and -0.5 * g0 >= g1 >= -2.0 * g0):
        return "i"
    if (g0 < 0 and g1 > -2.0 * g0) or (g0 > 0 and g1 < -2.0 * g0):
        return "ii"
    if (g0 > 0 and 0 > g1 > -0.5 * g0) or (g0 < 0 and 0 < g1 < -0.5 * g0):
        return "iii"
    return "iv"


def _g(g0: float, g1: float, x: float) -> float:
    sec = _sector(g0, g1)
    if sec == "origin":
        return 0.0
    if sec == "i":  # eq. (27)
        return g0 * (1 - 4 * x + 3 * x * x) + g1 * (-2 * x + 3 * x * x)
    if sec == "ii":  # eqs. (28)-(29)
        eta = (g1 + 2 * g0) / (g1 - g0)
        return g0 if x <= eta else g0 + (g1 - g0) * ((x - eta) / (1 - eta)) ** 2
    if sec == "iii":  # eqs. (30)-(31)
        eta = 3 * g1 / (g1 - g0)
        return g1 + (g0 - g1) * ((eta - x) / eta) ** 2 if x < eta else g1
    eta = g1 / (g1 + g0)  # sector (iv), eqs. (32)-(34)
    a = -g0 * g1 / (g0 + g1)
    if x <= eta:
        return a + (g0 - a) * ((eta - x) / eta) ** 2 if eta > 0 else g1
    return a + (g1 - a) * ((x - eta) / (1 - eta)) ** 2


def _G(g0: float, g1: float, x: float) -> float:
    """Integral of g from 0 to x (the paper leaves this to the reader, p. 77, step (6))."""
    sec = _sector(g0, g1)
    if sec == "origin":
        return 0.0
    if sec == "i":
        return g0 * (x - 2 * x * x + x ** 3) + g1 * (-x * x + x ** 3)
    if sec == "ii":
        eta = (g1 + 2 * g0) / (g1 - g0)
        return g0 * x if x <= eta else g0 * x + (g1 - g0) * (x - eta) ** 3 / (3 * (1 - eta) ** 2)
    if sec == "iii":
        eta = 3 * g1 / (g1 - g0)
        if x < eta:
            return g1 * x + (g0 - g1) * eta / 3 * (1 - ((eta - x) / eta) ** 3)
        return g1 * x + (g0 - g1) * eta / 3
    eta = g1 / (g1 + g0)
    a = -g0 * g1 / (g0 + g1)
    if x <= eta:
        return a * x + (g0 - a) * eta / 3 * (1 - ((eta - x) / eta) ** 3) if eta > 0 else g1 * x
    return a * x + (g0 - a) * eta / 3 + (g1 - a) * (x - eta) ** 3 / (3 * (1 - eta) ** 2)


# ---- instruments and pricing --------------------------------------------------

@dataclass(frozen=True)
class Deposit:
    """Simple-interest deposit from start to end at `rate`, Act/360."""
    name: str
    start: float
    end: float
    accrual: float
    rate: float


@dataclass(frozen=True)
class Ois:
    """Overnight-indexed swap. Each period k accrues from start[k] to end[k]
    (year fractions from the as-of date) with Act/360 accrual accrual[k] and
    pays at pay[k]. Under a single curve the compounded overnight leg of a
    period is worth (Z(start)/Z(end) - 1) Z(pay), because daily compounding of
    the curve's own overnight forwards telescopes to the ratio of discount
    factors; the par rate equates the two legs."""
    name: str
    start: tuple[float, ...]
    end: tuple[float, ...]
    pay: tuple[float, ...]
    accrual: tuple[float, ...]
    rate: float
    pillar: float


def ois_par_rate(curve, inst: Ois) -> float:
    z = curve.discount
    float_leg = sum((z(s) / z(e) - 1.0) * z(p) for s, e, p in zip(inst.start, inst.end, inst.pay))
    annuity = sum(a * z(p) for a, p in zip(inst.accrual, inst.pay))
    return float_leg / annuity


def bootstrap(deposits: list[Deposit], swaps: list[Ois], method: str = "monotone_convex",
              positive: bool = True, tol: float = 1e-14):
    """Return the curve (MonotoneConvex or LogLinearDiscount) that reprices every
    deposit and swap. Deposits must be contiguous from the as-of date; each ends
    on a node. Swap pillars are the remaining nodes, in increasing order."""
    t = [0.0]
    fd_dep = []
    for d in deposits:
        if abs(d.start - t[-1]) > 1e-12:
            raise ValueError(f"deposit {d.name} does not start on the previous node")
        fd_dep.append(math.log(1.0 + d.rate * d.accrual) / (d.end - d.start))
        t.append(d.end)
    pillars = [s.pillar for s in swaps]
    if any(b <= a for a, b in zip([t[-1]] + pillars, pillars)):
        raise ValueError("swap pillars must be increasing and after the last deposit")
    t += pillars
    cls = MonotoneConvex if method == "monotone_convex" else LogLinearDiscount

    def build(x):
        fd = fd_dep + list(x)
        return cls(t, fd, positive) if cls is MonotoneConvex else cls(t, fd)

    def residuals(x):
        c = build(x)
        return [ois_par_rate(c, s) - s.rate for s in swaps]

    # Start from each swap's rate as a flat forward and solve the square system.
    x0 = np.array([s.rate for s in swaps])
    sol = root(residuals, x0, method="hybr", tol=tol, options={"xtol": tol, "maxfev": 20000})
    worst = max(abs(r) for r in residuals(sol.x))
    if worst > 1e-11:
        raise RuntimeError(f"{method} bootstrap did not converge: max par-rate residual {worst:.3e} ({sol.message})")
    return build(sol.x)
