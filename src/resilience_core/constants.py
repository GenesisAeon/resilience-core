"""Physical and mathematical constants for resilience-core."""

SIGMA: float = 2.2
"""Default UTAC coupling constant σ used in tanh(σΓ)."""

SIGMA_PHI: float = 1.0 / 16.0
"""Frame-Principle boundary σ_Φ ≈ 0.0625 — Ρ below this signals near-collapse."""

GAMMA_MAX: float = 0.920
"""Maximum observed Γ in the CREP Atlas (ERA5 Arctic — most saturated system)."""

C_CRITICAL: float = 0.5
"""Default critical coupling load above which inter-domain destabilisation dominates."""

COLLAPSE_THRESHOLD: float = SIGMA_PHI
"""Ρ < COLLAPSE_THRESHOLD → near-collapse warning."""

# Calibrated reference values from CREP Atlas
BENCHMARK_GAMMA: dict[str, float] = {
    "amoc": 0.251,
    "arctic_era5": 0.920,
    "sandpile": 0.296,
    "quantum": 0.050,
}

BENCHMARK_RHO: dict[str, float] = {
    "amoc": 0.65,
    "arctic_era5": 0.05,
    "sandpile": 0.75,
    "quantum": 0.90,
}
