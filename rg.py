"""rg.py — AMG-local port of reconstruction_gate.h.

Named machine: rg_reconstruct.
Not a new title. Not a restore of the RG pin twin.
RG.chi lives here. Do not XOR into DCL.chi.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum


class RGVerdict(IntEnum):
    ACCEPT = 0
    REWRITE = 1
    REJECT = 2


@dataclass
class RGState:
    d: float = 0.0
    c: float = 1.0
    lambda_: float = 0.55
    chi: int = 1
    r_chi: float = 0.0
    steps_since_flip: int = 99
    joint_hold: int = 0


@dataclass(frozen=True)
class RGParams:
    alpha: float = 0.45
    beta: float = 0.06
    gamma: float = 0.50
    delta: float = 0.45
    eta: float = 0.06
    tau: float = 0.18
    theta: float = 0.30
    alpha_r: float = 0.20
    reject_floor: float = 0.10
    accept_relevance: float = 0.30
    flip_cooldown: int = 6
    flip_hold: int = 3


RG_DEFAULTS = RGParams()


def rg_init() -> RGState:
    return RGState()


def rg_reconstruct(s: RGState, par: RGParams,
                   draft_d: float, draft_c: float, draft_corr: float):
    rho = s.d * s.c
    diff = abs(draft_d - s.d)
    if diff > 1.0:
        diff = 1.0
    relevance = draft_corr * (1.0 - 0.75 * diff)

    rigidity = 0.0
    if s.lambda_ > 0.40 and draft_corr > par.tau:
        sign = 1.0 if s.chi == 0 else -1.0
        rigidity = sign * s.lambda_ * (1.0 - s.lambda_)

    lam = (s.lambda_
           + par.alpha * rho * (1.0 - s.lambda_)
           - par.beta * (1.0 - s.c) * s.lambda_
           + par.delta * rigidity
           + par.gamma * relevance * s.lambda_ * (1.0 - s.lambda_))
    if lam < 0.15:
        lam = 0.15
    if lam > 1.0:
        lam = 1.0

    att = 1.0 - par.eta * lam
    s.d = s.d * att + (1.0 - att) * draft_d
    s.c = s.c * att + (1.0 - att) * draft_c
    s.lambda_ = lam
    s.steps_since_flip += 1

    joint = (lam > 0.55 and draft_corr > par.tau and relevance > 0.22)
    if joint:
        s.joint_hold += 1
    else:
        s.joint_hold = 0
    if s.joint_hold >= par.flip_hold and s.steps_since_flip >= par.flip_cooldown:
        s.chi ^= 1
        s.steps_since_flip = 0
        s.joint_hold = 0

    ss = 1.0 if s.chi == 1 else -1.0
    s.r_chi = (1.0 - par.alpha_r) * s.r_chi + par.alpha_r * ss

    if relevance < par.reject_floor:
        return RGVerdict.REJECT, s.d, s.c
    if s.chi == 1 and lam >= par.theta and relevance >= par.accept_relevance:
        return RGVerdict.ACCEPT, draft_d, draft_c
    keep = relevance
    if keep < 0.0:
        keep = 0.0
    if keep > 1.0:
        keep = 1.0
    out_d = keep * draft_d + (1.0 - keep) * s.d
    out_c = keep * draft_c + (1.0 - keep) * s.c
    return RGVerdict.REWRITE, out_d, out_c
