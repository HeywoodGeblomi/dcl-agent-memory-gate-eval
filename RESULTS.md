# Recorded results

Transcribed from `DONE.md` in HeywoodGeblomi/dcl-agent-memory-gate. These numbers were not re-run for this review copy. The source repo had no results JSON. A structured copy is in `results.json`.

Standing key: `repo.dcl-agent-memory-gate.claim`

Claim text: "toy harness: dual residual gates DCL χ on memory writes; not production."

Thresholds stay locked: 0.04 / 0.005 / 0.1 / 0.2.

| Track | Result | Counts |
| --- | --- | --- |
| live_refuse | dual-residual git insertions. Claim kept. | n=33, confirm 0/33, gated χ 0, frozen χ 0 |
| live_git_confirm | BLOCKED: insertions have σ_Δ ≈ 0; overlay correctly refuses | not a completed confirm stream |
| track_A_fixture_confirm | noisy_ramp_confirmed T=256 seed=42 amp=15 as r[i], claim as value. Label: fixture, not kitchen work. | gated χ 1 / flips 139 / λ 0.698; frozen χ 0 / 0 / 0.795; confirm/refuse 143/113 |
| track_B_kitchen_r_corr | residual-sublation `dcl_harness.realistic_residual_scenario` column `r_corr` T=150 seed=42. residual/d/y/x refuse (σ_Δ=0). r_corr owns: clas 0.993 σ_Δ -0.0435. Label: kitchen DCL plant r_corr, not live git, not the ramp. | gated χ 1 / flips 3 / λ 0.393; frozen χ 0 / 0 / 0.801; confirm/refuse 45/105 |
| audit_only_filesize_confirm | demoted | not a claim |
| kill_b |  | not a claim |

Wrap from the source: A then B recorded. NON_CLAIMS.md still wins.

The built-in `parity_trap` scenario is part of `demo.py`, but `DONE.md` does not record a numeric SCOREBOARD for it, so none is listed here.
