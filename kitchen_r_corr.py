"""kitchen_r_corr.py — Track B generator only.

Column r_corr from residual-sublation dcl_harness.realistic_residual_scenario.
Kitchen DCL plant. Not live git. Not noisy_ramp_confirmed.
Do not treat this as a work-log confirm.
"""
from __future__ import annotations

import numpy as np


def realistic_residual_scenario(T: int = 150, seed: int = 42, noise_scale: float = 1.0):
    """Scalar plant + progressive sensor bias + intermittent polarity disturbance.

    Copied from HeywoodGeblomi/residual-sublation dcl_harness.py so Lucas can
    persist Track B without cloning that private tree.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(T)
    a = 0.92
    x = np.zeros(T)
    for i in range(1, T):
        x[i] = a * x[i - 1] + rng.normal(0.0, 0.01 * noise_scale)
    bias = 0.004 * t
    true_pol = np.zeros(T, dtype=int)
    pol = 0
    flip_times = [ft for ft in (40, 70, 100, 130) if ft < T]
    for i in range(1, T):
        if i in flip_times:
            pol ^= 1
        true_pol[i] = pol
    disturb = 0.25 * (2 * true_pol - 1) * (t > 30)
    y = x + bias + disturb + rng.normal(0.0, 0.05 * noise_scale, T)
    xhat = np.zeros(T)
    residual = np.zeros(T)
    for i in range(1, T):
        xhat[i] = a * xhat[i - 1]
        residual[i] = y[i] - xhat[i]
        xhat[i] = 0.7 * xhat[i] + 0.3 * y[i]
    d = np.clip(np.abs(residual) / 1.5, 0.0, 1.0)
    c = np.clip(
        1.0 - 0.7 * (bias / (bias[-1] + 1e-8)) + rng.normal(0.0, 0.02 * noise_scale, T),
        0.05,
        1.0,
    )
    r_corr = np.clip(
        0.15
        + 0.55 * np.abs(np.gradient(residual)) * 5.0
        + 0.40 * np.isin(t, flip_times).astype(float),
        0.0,
        1.0,
    )
    return {
        "d": d,
        "c": c,
        "r_corr": r_corr,
        "true_pol": true_pol,
        "x": x,
        "residual": residual,
        "t": t,
    }


def r_corr_series(T: int = 150, seed: int = 42):
    return realistic_residual_scenario(T=T, seed=seed)["r_corr"]
