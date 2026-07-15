"""Inter-domain coupling matrix C_ij.

C_ij(t) = influence of domain j on dΓ_i/dt.
Positive = destabilising (accelerates drift of Γ_i toward Γ_max).
Negative = stabilising (damps Γ_i drift).
"""

from __future__ import annotations

from resilience_core.constants import C_CRITICAL, GAMMA_MAX


class CouplingMatrix:
    """Registry of pairwise coupling effects between GenesisAeon domains."""

    def __init__(self, c_critical: float = C_CRITICAL) -> None:
        self.c_critical = c_critical
        self._couplings: dict[tuple[str, str], float] = {}

    def register_coupling(
        self, source_domain: str, target_domain: str, effect: float
    ) -> None:
        """Register a coupling effect.

        Args:
            source_domain: Domain driving the perturbation.
            target_domain: Domain whose Γ-rate is affected.
            effect: Coupling strength. Positive = destabilising.
        """
        self._couplings[(source_domain, target_domain)] = effect

    def remove_coupling(self, source_domain: str, target_domain: str) -> None:
        """Remove a previously registered coupling."""
        self._couplings.pop((source_domain, target_domain), None)

    def total_load(self, target_domain: str) -> float:
        """Sum of destabilising (positive) C_ij contributions for *target_domain*.

        Stabilising couplings (negative effect) are excluded: they reduce drift
        and do not add to collapse risk. Using abs() here would incorrectly
        penalise stabilising sources and reverse the documented sign semantics.
        """
        return sum(
            v
            for (src, tgt), v in self._couplings.items()
            if tgt == target_domain and v > 0
        )

    def coupling_factor(self, target_domain: str) -> float:
        """1 - total_load / C_critical, clipped to [0, 1]."""
        return max(0.0, 1.0 - self.total_load(target_domain) / self.c_critical)

    def coupling_sources(self, target_domain: str) -> dict[str, float]:
        """Return {source: effect} for all sources of *target_domain*."""
        return {
            src: effect
            for (src, tgt), effect in self._couplings.items()
            if tgt == target_domain
        }

    def cascade_threshold(
        self, target_domain: str, gamma: float, gamma_max: float = GAMMA_MAX
    ) -> bool:
        """True when cascade collapse is imminent.

        Condition: coupling load > 50 % of C_critical AND Γ > 95 % of Γ_max.
        """
        load = self.total_load(target_domain)
        return load > self.c_critical * 0.5 and gamma > gamma_max * 0.95
