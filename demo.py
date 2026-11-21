"""demo.py — baseline vs gated vs frozen-χ.

Two scenarios:
1. parity_trap — Dual Residual refuses the whole stream (gate correctness).
2. residual_confirm — borderline noisy_ramp (dual-residual suite) so Dual
   Residual confirms on real windows and gated χ can move.

Do not invent numbers. Run this file.
"""
from __future__ import annotations

import argparse

import numpy as np

from memory_baseline import BaselineMemory
from memory_gated import GatedMemory


def parity_trap_scenario(T: int = 120, seed: int = 0):
    rng = np.random.default_rng(seed)
    t = np.arange(T)
    d = np.clip(0.35 + 0.05 * np.sin(2 * np.pi * t / 25.0) + rng.normal(0, 0.03, T), 0, 1)
    c = np.clip(0.70 - 0.002 * t + rng.normal(0, 0.02, T), 0.05, 1)
    r_corr = np.clip(
        0.12
        + 0.10 * (np.sin(2 * np.pi * t / 18.0) > 0.4).astype(float)
        + rng.normal(0, 0.04, T),
        0,
        1,
    )
    true_pol = np.zeros(T, dtype=int)
    pol = 0
    flips = [ft for ft in (30, 55, 80, 105) if ft < T]
    for i in range(T):
        if i in flips:
            pol ^= 1
        true_pol[i] = pol
    return {
        "name": "parity_trap",
        "d": d,
        "c": c,
        "r_corr": r_corr,
        "true_pol": true_pol,
        "flips": flips,
        "blurb": f"Parity-trap: {T} steps, scheduled hidden flips at {flips}",
    }


def noisy_ramp_confirmed(n: int = 256, seed: int = 42, amp: int = 15) -> np.ndarray:
    """Borderline dual-owned generator from HeywoodGeblomi/dual-residual.

    C++ reference (tests/generators.hpp):
        a[i] = i + (rng() % (2 * amp) - amp);  // seed 42, amp 15

    Uses NumPy MT19937(seed). Full-length evidence may differ from the C++
    oracle on n=1024; sliding windows of 64 (the gated history length) confirm.
    """
    rng = np.random.Generator(np.random.MT19937(seed))
    # C++: rng() % (2*amp) - amp  →  [-amp, amp-1]
    noise = rng.integers(0, 2 * amp, size=n, dtype=np.int64) - amp
    return np.arange(n, dtype=np.float64) + noise.astype(np.float64)


def residual_confirm_scenario(T: int = 256, seed: int = 42):
    """Stream where Dual Residual confirms on real windows."""
    d = noisy_ramp_confirmed(n=T, seed=seed, amp=15)
    t = np.arange(T)
    c = np.clip(0.70 - 0.001 * t, 0.05, 1.0)
    # Keep r_corr above DCL tau (0.20) so confirmed steps can actually flip χ.
    r_corr = np.full(T, 0.50)
    return {
        "name": "residual_confirm",
        "d": d,
        "c": c,
        "r_corr": r_corr,
        "true_pol": None,
        "flips": [],
        "blurb": (
            f"Residual-confirm: noisy_ramp_confirmed T={T} seed={seed} amp=15 "
            f"(dual-residual borderline suite)"
        ),
    }


def _flip_count(log):
    return sum(1 for j in range(1, len(log)) if log[j] != log[j - 1])


def run_scenario(sc):
    d, c, rc = sc["d"], sc["c"], sc["r_corr"]
    true_pol, flips = sc["true_pol"], sc["flips"]
    base = BaselineMemory()
    gated = GatedMemory(freeze=False)
    frozen = GatedMemory(freeze=True)
    print(sc["blurb"])
    if true_pol is not None:
        print(f"{'step':>5} {'true':>5} {'base':>8} {'chi':>5} {'frz':>5} {'own':>5}")
    else:
        print(f"{'step':>5} {'base':>10} {'chi':>5} {'frz':>5} {'own':>5}")
    for i in range(len(d)):
        base.write("residual", float(d[i]))
        g = gated.observe("residual", float(d[i]), float(d[i]), float(c[i]), float(rc[i]))
        f = frozen.observe("residual", float(d[i]), float(d[i]), float(c[i]), float(rc[i]))
        mark = (i % 32 == 0) or (i in flips) or (i == len(d) - 1)
        if mark:
            if true_pol is not None:
                print(
                    f"{i:>5} {true_pol[i]:>5} {float(d[i]):>8.3f} "
                    f"{g['chi']:>5} {f['chi']:>5} {str(g['dual_confirmed']):>5}"
                )
            else:
                print(
                    f"{i:>5} {float(d[i]):>10.3f} "
                    f"{g['chi']:>5} {f['chi']:>5} {str(g['dual_confirmed']):>5}"
                )
    gs = gated.snapshot()
    fs = frozen.snapshot()
    print()
    print(f"SCOREBOARD [{sc['name']}]")
    print(f"  baseline last visible d     {base.snapshot()['residual']:.4f}")
    print(
        f"  gated χ / flips / λ         "
        f"{gs['chi_log'][-1]} / {_flip_count(gs['chi_log'])} / {gs['lambda']:.3f}"
    )
    print(
        f"  frozen χ / flips / λ        "
        f"{fs['chi_log'][-1]} / {_flip_count(fs['chi_log'])} / {fs['lambda']:.3f}"
    )
    print(f"  gated dual confirm/refuse   {gs['confirmed_steps']} / {gs['refused_steps']}")
    print()
    return {
        "name": sc["name"],
        "baseline_last_d": float(base.snapshot()["residual"]),
        "gated_chi": gs["chi_log"][-1],
        "gated_flips": _flip_count(gs["chi_log"]),
        "gated_lambda": float(gs["lambda"]),
        "frozen_chi": fs["chi_log"][-1],
        "frozen_flips": _flip_count(fs["chi_log"]),
        "frozen_lambda": float(fs["lambda"]),
        "confirmed": gs["confirmed_steps"],
        "refused": gs["refused_steps"],
    }


def run(scenarios=None):
    if scenarios is None:
        scenarios = ["parity_trap", "residual_confirm"]
    builders = {
        "parity_trap": parity_trap_scenario,
        "residual_confirm": residual_confirm_scenario,
    }
    results = []
    for name in scenarios:
        results.append(run_scenario(builders[name]()))
    print("Baseline overwrites. Frozen χ cannot leave 0. Gated can — when Dual Residual confirms.")
    print("That is the hole. This is the nail. Not LangGraph. Not production.")
    return results


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="DCL memory-gate demo")
    p.add_argument(
        "--scenario",
        choices=("parity_trap", "residual_confirm", "both"),
        default="both",
        help="which scenario(s) to run (default: both)",
    )
    args = p.parse_args()
    names = (
        ["parity_trap", "residual_confirm"]
        if args.scenario == "both"
        else [args.scenario]
    )
    run(names)
