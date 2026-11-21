"""dual_residual.py — pure-Python port of the locked C++ oracle.

Thresholds are immutable. Do not parameterize.
Classical disorder + σ_Δ (even-indexed event parity) must jointly confirm.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from enum import IntEnum

CLASSICAL_OWNED_THRESH = 0.04
SECOND_SOLID_FLOOR = 0.005
TALENT2_SIGMA_THRESH = 0.1
TALENT3_CLASSICAL = 0.2
SAMPLE_SIZE = 512
MAX_EVENTS = 512

class Talent(IntEnum):
    None_ = 0
    T1 = 1
    T2 = 2
    T3 = 3

@dataclass
class Evidence:
    confirmed: bool = False
    sigma_delta: float = 0.0
    classical: float = 0.0
    suggested: Talent = Talent.None_

def _polarity_stream(a: np.ndarray, stride: int = 1) -> np.ndarray:
    n = len(a)
    out = []
    for i in range(0, n - stride):
        if a[i + stride] > a[i]:
            out.append(1.0)
        elif a[i + stride] < a[i]:
            out.append(-1.0)
        else:
            out.append(0.0)
    return np.array(out, dtype=float)

def _compute_sigma(stream: np.ndarray) -> tuple[float, float, int]:
    T = len(stream)
    if T < 4:
        return 0.0, 0.0, 0
    # event indices: where polarity changes
    events = []
    above = stream[0] > 0
    for t in range(1, T):
        now = stream[t] > 0
        if now != above:
            events.append(t)
            above = now
    ne = len(events)
    if ne < 4:
        return 0.0, 0.0, 0
    even_idx = events[0::2]
    no = len(even_idx)
    if no < 2:
        return 0.0, 0.0, 0
    even_vals = stream[even_idx]
    # alternate even/odd within the even-indexed events
    sum_even = even_vals[0::2].sum()
    n_even = len(even_vals[0::2])
    sum_odd = even_vals[1::2].sum()
    n_odd = len(even_vals[1::2])
    even_mean = sum_even / n_even if n_even else 0.0
    odd_mean = sum_odd / n_odd if n_odd else 0.0
    delta = even_mean - odd_mean
    return delta, float(np.mean(np.abs(stream))), no

def evidence(a: np.ndarray, classical_thresh: float = CLASSICAL_OWNED_THRESH,
             sigma_floor: float = SECOND_SOLID_FLOOR) -> Evidence:
    a = np.asarray(a, dtype=float)
    n = len(a)
    if n < 2:
        return Evidence()
    stride = max(1, n // SAMPLE_SIZE) if n > 1024 else 1
    stream = _polarity_stream(a, stride)
    if len(stream) < 4:
        return Evidence()
    sigma_delta, classical, _ = _compute_sigma(stream)
    classical_owned = classical > classical_thresh
    confirmed = classical_owned and abs(sigma_delta) >= sigma_floor
    if not confirmed:
        suggested = Talent.None_
    elif abs(sigma_delta) > TALENT2_SIGMA_THRESH:
        suggested = Talent.T2
    elif classical > TALENT3_CLASSICAL:
        suggested = Talent.T3
    else:
        suggested = Talent.T1
    return Evidence(confirmed=confirmed, sigma_delta=sigma_delta,
                    classical=classical, suggested=suggested)
