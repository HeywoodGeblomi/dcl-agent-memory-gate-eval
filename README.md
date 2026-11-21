# DCL agent memory gate eval

Heywood Geblomi (Walter Howard)

This is a review copy of a toy agent-memory gate evaluation. The original private pin, [HeywoodGeblomi/dcl-agent-memory-gate](https://github.com/HeywoodGeblomi/dcl-agent-memory-gate), was left unchanged.

## What it is

A small Python harness that compares three memory agents on the same residual stream:

- Baseline: last visible residual only. Each new value overwrites the last.
- Gated: Dual Residual must confirm before DCL may flip a hidden bit chi (χ).
- Frozen-chi ablation: the same gate, but chi is forced to stay 0.

It is weekend-scale wiring, not a product and not a LangGraph integration. [NON_CLAIMS.md](NON_CLAIMS.md) wins on conflict.

## What the eval measured

Recorded numbers are copied from `DONE.md` in the source repo. They were not re-run for this copy, and the source repo had no results JSON. The same figures are in [RESULTS.md](RESULTS.md) and [results.json](results.json).

Standing claim text from the source: "toy harness: dual residual gates DCL χ on memory writes; not production."

Dual Residual thresholds stay locked at 0.04 / 0.005 / 0.1 / 0.2.

Conditions and metrics:

- A refuse stream should keep gated chi at 0 and frozen chi at 0.
- A confirm stream should split gated chi from frozen chi (frozen stays 0).
- Metrics: Dual Residual confirm or refuse counts, gated and frozen chi, flip counts, and lambda.

Recorded tracks:

| Track | Result |
| --- | --- |
| live_refuse | dual-residual git insertions n=33, confirm 0/33, gated χ 0, frozen χ 0, claim kept |
| live_git_confirm | BLOCKED: insertions have σ_Δ ≈ 0; overlay correctly refuses |
| track_A_fixture_confirm | noisy_ramp_confirmed T=256 seed=42 amp=15 as r[i], claim as value. gated χ 1 / flips 139 / λ 0.698; frozen χ 0 / 0 / 0.795; confirm/refuse 143/113. Label: fixture, not kitchen work. |
| track_B_kitchen_r_corr | residual-sublation `dcl_harness.realistic_residual_scenario` column `r_corr` T=150 seed=42. residual/d/y/x refuse (σ_Δ=0). r_corr owns: clas 0.993 σ_Δ -0.0435. observe on claim: gated χ 1 / flips 3 / λ 0.393; frozen χ 0 / 0 / 0.801; confirm/refuse 45/105. Label: kitchen DCL plant r_corr, not live git, not the ramp. |
| audit_only_filesize_confirm | demoted, not a claim |
| kill_b | not a claim |

`python demo.py` runs two built-in scenarios, `parity_trap` and `residual_confirm` (the Track A fixture). Track B used `kitchen_r_corr.py` and is not wired into that default run. The source `DONE.md` does not record a numeric SCOREBOARD for `parity_trap`, so none is invented here.

## What it did not claim

Read [NON_CLAIMS.md](NON_CLAIMS.md) in full. In short:

- Toy scale. Not production. Not a performance claim. Not a filed title.
- No unit tests and no CI.
- No hashed preregistration.
- No injection detection and no false-hold measurement.
- The live-git confirm stream was blocked: insertions had σ_Δ about 0, and the overlay correctly refused.
- Possession of this demo is not a commercial license for Dual Residual, DCL, or Reconstruction Gate.
- The source repository has no LICENSE file. This copy adds none.

## How to run

```bash
pip install -r requirements.txt
python demo.py
```

Needs numpy. Optional: `python demo.py --scenario residual_confirm` or `python demo.py --scenario parity_trap`.

The printed SCOREBOARD lines are a fresh local run. The numbers in RESULTS.md are the recorded source figures, not a fresh SCOREBOARD from this copy.

## Files

| File | Role |
| --- | --- |
| `dual_residual.py` | Python port of the public Dual Residual oracle. Thresholds locked. |
| `dcl.py` | Hard DCL step and commit. |
| `rg.py` | Local port of `rg_reconstruct`. Read path only. |
| `memory_baseline.py` | Overwrite store. |
| `memory_gated.py` | Confirm then commit. Read path calls `rg_reconstruct` beside DCL chi. |
| `demo.py` | Parity-trap plus residual-confirm plus freeze ablation. |
| `kitchen_r_corr.py` | Track B generator only. Not called by `python demo.py`. |
| `requirements.txt` | numpy>=1.24 |
| `DONE.md` | Unedited source record of the numbers. |
| `RESULTS.md` / `results.json` | Table and JSON transcribed from DONE.md. Not a re-run. |
| `NON_CLAIMS.md` | Honesty file, copied verbatim. Wins on conflict.
