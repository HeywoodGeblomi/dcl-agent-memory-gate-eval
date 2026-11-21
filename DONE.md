# Done when

Private gated-memory loop. Not a public grant. NON_CLAIMS.md wins on conflict.

- Standing key: `repo.dcl-agent-memory-gate.claim`
- Refuse stream: real git work (insertions / timestamp deltas) must keep gated χ = 0 and frozen χ = 0
- Confirm stream: a series from our private work logs or repo activity, NOT `noisy_ramp_confirmed` seed 42 amp 15
- Finish line: refuse stream does not flip χ; confirm stream splits gated χ vs frozen χ; this file plus NON_CLAIMS.md still hold

Thresholds stay locked: 0.04 / 0.005 / 0.1 / 0.2. Do not edit `dual_residual.py` to chase a flip.

## Status

- standing key: `repo.dcl-agent-memory-gate.claim`
- claim text: "toy harness: dual residual gates DCL χ on memory writes; not production."
- live_refuse: dual-residual git insertions n=33, confirm 0/33, gated χ 0, frozen χ 0, claim kept
- live_git_confirm: BLOCKED — insertions have σ_Δ ≈ 0; overlay correctly refuses
- track_A_fixture_confirm: noisy_ramp_confirmed T=256 seed=42 amp=15 as r[i], claim as value=. gated χ 1 / flips 139 / λ 0.698; frozen χ 0 / 0 / 0.795; confirm/refuse 143/113. Label: fixture, not kitchen work.
- track_B_kitchen_r_corr: residual-sublation `dcl_harness.realistic_residual_scenario` column `r_corr` T=150 seed=42. residual/d/y/x refuse (σ_Δ=0). r_corr owns: clas 0.993 σ_Δ -0.0435. observe on claim: gated χ 1 / flips 3 / λ 0.393; frozen χ 0 / 0 / 0.801; confirm/refuse 45/105. Label: kitchen DCL plant r_corr, not live git, not the ramp.
- audit_only_filesize_confirm: demoted, not a claim
- kill_b: not a claim
- wrap: A then B recorded. NON_CLAIMS.md still wins.
