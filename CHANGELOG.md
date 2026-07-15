# Changelog

All notable changes to `resilience-core` (P40) are documented here.

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
