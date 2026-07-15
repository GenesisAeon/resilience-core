"""Systemresilienzgröße Ρ = |λ*| · (1 - Γ/Γ_max) · coupling_factor."""

from __future__ import annotations

from dataclasses import dataclass, field

from resilience_core.constants import COLLAPSE_THRESHOLD, GAMMA_MAX, SIGMA_PHI
from resilience_core.coupling import CouplingMatrix
from resilience_core.eigenrate import ResilienceEigenrate


@dataclass
class ResilienceState:
    """Full resilience snapshot for a UTAC domain at time t."""

    rho: float
    lambda_star: float
    criticality_margin: float
    coupling_load: float
    near_collapse: bool
    coupling_sources: dict[str, float] = field(default_factory=dict)


class RhoCalculator:
    """Computes Ρ = |λ*| · (1 - Γ/Γ_max) · coupling_factor(domain).

    Calibrated reference values (CREP Atlas):
      AMOC    (Γ=0.251): Ρ ≈ 0.65
      Arctic  (Γ=0.920): Ρ ≈ 0.05
      Sandpile(Γ=0.296): Ρ ≈ 0.75
      Quantum (Γ=0.050): Ρ ≈ 0.90

    Frame-Principle boundary: Ρ → 0 when Γ → 1 - σ_Φ ≈ 0.9375
    """

    SIGMA_PHI: float = SIGMA_PHI
    GAMMA_MAX: float = GAMMA_MAX
    COLLAPSE_THRESHOLD: float = COLLAPSE_THRESHOLD

    def __init__(
        self, eigenrate: ResilienceEigenrate, coupling: CouplingMatrix
    ) -> None:
        self.eigenrate = eigenrate
        self.coupling = coupling

    def compute(self, gamma: float, domain: str) -> ResilienceState:
        """Compute full ResilienceState for *domain* at current Γ."""
        lam = self.eigenrate.compute(gamma)
        crit_margin = max(0.0, 1.0 - gamma / self.GAMMA_MAX)
        coup_factor = self.coupling.coupling_factor(domain)
        rho = lam * crit_margin * coup_factor

        return ResilienceState(
            rho=rho,
            lambda_star=lam,
            criticality_margin=crit_margin,
            coupling_load=1.0 - coup_factor,
            near_collapse=rho < self.COLLAPSE_THRESHOLD,
            coupling_sources=self.coupling.coupling_sources(domain),
        )
