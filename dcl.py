"""dcl.py — port of dynamic_commitment.h (hard DCL v0.2.1).

Hidden variable χ that stores forbidden memory, collapses ambiguity, and
maintains an internal model. Non-reducible to any function of (d, c) alone.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class DCLParams:
    alpha: float = 0.25
    beta: float = 0.08
    gamma: float = 0.30
    delta: float = 0.55
    eta: float = 0.10
    mu: float = 0.08
    kappa: float = 1.2
    tau: float = 0.20
    theta: float = 0.35

@dataclass
class DCLState:
    d: float = 0.0
    c: float = 1.0
    lambda_: float = 0.0
    chi: int = 0

def dcl_init() -> DCLState:
    return DCLState()

def dcl_step(s: DCLState, par: DCLParams, r_fresh: float, k_fresh: float, r_corr: float,
              force_chi: int | None = None) -> None:
    rho = s.d * s.c
    rigidity = 0.0
    if s.lambda_ > 0.4 and r_corr > par.tau:
        sign = 1.0 if s.chi == 0 else -1.0
        rigidity = sign * s.lambda_ * (1.0 - s.lambda_)
    lambda_new = (s.lambda_
                  + par.alpha * rho * (1.0 - s.lambda_)
                  - par.beta * (1.0 - s.c) * s.lambda_
                  + par.delta * rigidity
                  + par.gamma * r_corr * (0.6 - s.lambda_))
    lambda_new = max(0.0, min(1.0, lambda_new))
    att = 1.0 - par.eta * lambda_new
    pol = 1.0 if s.chi == 0 else -1.0
    s.d = s.d * att + (1.0 - att) * r_fresh + 0.12 * pol * max(rigidity, 0.05) * s.lambda_
    s.d = max(0.0, min(1.0, s.d))
    s.c = s.c * att + (1.0 - att) * k_fresh
    s.c = max(0.05, min(1.0, s.c))
    if force_chi is None:
        if lambda_new > 0.45 and r_corr > par.tau:
            s.chi ^= 1
    else:
        s.chi = int(force_chi)
    s.lambda_ = lambda_new

def dcl_commit(s: DCLState, par: DCLParams, r_corr: float) -> bool:
    if s.lambda_ <= par.theta:
        return False
    discharge = par.mu * (s.lambda_ - par.theta) * (1.0 + par.kappa * r_corr)
    s.lambda_ = max(0.0, s.lambda_ - discharge)
    return True
