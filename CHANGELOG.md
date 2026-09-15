# Changelog

All notable changes to `resilience-core` (P40) are documented here.

## [1.0.1] — 2026-09-15

### Fixed (documentation / test honesty, no behavior change)
- `benchmarks/arctic_calibration.py` and `benchmarks/sandpile_calibration.py`
  now report their calibration status honestly, matching the existing
  `amoc_calibration.py` pattern: `rho_with_default_r`, `rho_atlas_target`,
  and an explicit `calibration_status` field, instead of a misleading
  `rho_in_range` check against an uncalibrated default. Both scripts
  previously claimed the CREP-Atlas target values (Ρ≈0.05, Ρ≈0.75) were
  reachable with default parameters; running them showed `rho_in_range:
  false` in both cases, undetected because neither script was wired into
  the automated test suite.
- Arctic case specifically: `GAMMA_MAX` (0.920) is identical to the Arctic
  ERA5 benchmark Γ itself, so the criticality margin is structurally zero
  there for any `r` — documented with a Known-Issue comment in
  `constants.py` (value unchanged), and `arctic_calibration.py` now
  reports this explicitly instead of an undefined `r_required_for_target`.
- Sandpile case: computed and documented `r_required_for_target ≈ 3.37`
  (analogous to AMOC's `r≈3.54`), calibration marked `OPEN — pending real
  sandpile/SOC coupling data`.
- `__init__.py` quick-start docstring corrected: the `compute_rho(gamma=
  0.920, domain="arctic")` example previously claimed `# ≈ 0.05`; the
  actual default-parameter result is `0.0` (see above).
- Added `tests/test_calibration_scripts.py`: exercises all three
  calibration runners (AMOC/Arctic/Sandpile) and asserts their
  `calibration_status` reporting is present and consistent — does not
  assert that default-`r` Ρ hits the CREP-Atlas targets, since that
  requires domain-specific calibration not yet available.

No constants changed (`GAMMA_MAX`, `SIGMA`, `SIGMA_PHI`, `C_CRITICAL` all
unchanged); 107/108 tests pass (one pre-existing, unrelated CLI
version-string failure tracked separately, not introduced by this
release — see `crep-utac-afet-formalism/FOLLOWUP_TICKETS.md`).

## [1.0.0] — 2026-07-15

### Added
- `ResilienceEigenrate`: UTAC fixpoint eigenrate |λ*| = r·tanh²(σΓ)
- `CouplingMatrix`: inter-domain C_ij coupling registry with cascade threshold
- `CascadeDetector`: multi-source cascade collapse detection
- `RhoCalculator`: Ρ = |λ*|·(1-Γ/Γ_max)·coupling_factor
- `ResilienceCore`: Diamond Interface main class with all 6 methods including
  `get_resilience_state()` as the new 6th Diamond method
- `frame_principle.py`: σ_Φ ≈ 1/16 boundary analysis
- `compute_rho()` convenience function
- Calibration benchmarks for AMOC, Arctic ERA5, Sandpile SOC
- Full test suite (eigenrate, coupling, Ρ, frame-principle, diamond compliance)
- Diamond-validation CI workflow

### Mathematical Foundation
- UTAC-ODE fixpoint: H* = K·tanh(σΓ), λ* = −r·tanh²(σΓ)
- Ρ(t) = |λ*(t)| · (1−Γ/Γ_max) · (1−Σ|C_ij|/C_critical)
- Frame-Principle limit: Ρ→0 when Γ→Γ_max·(1−σ_Φ) AND coupling→C_critical

### Calibrated Reference Values
| Domain | Γ | Ρ |
|--------|---|---|
| Quantum bit | 0.050 | ≈ 0.90 |
| Sandpile SOC | 0.296 | ≈ 0.75 |
| AMOC | 0.251 | ≈ 0.65 |
| Arctic ERA5 | 0.920 | ≈ 0.05 |
