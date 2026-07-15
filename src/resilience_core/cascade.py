"""Cascade detection — multiple weak couplings converging on a near-critical domain."""

from __future__ import annotations

from dataclasses import dataclass, field

from resilience_core.constants import C_CRITICAL, GAMMA_MAX
from resilience_core.coupling import CouplingMatrix


@dataclass
class CascadeEvent:
    target_domain: str
    gamma: float
    total_coupling_load: float
    active_sources: dict[str, float] = field(default_factory=dict)
    severity: str = "warning"  # "warning" | "critical"


class CascadeDetector:
    """Detects when multiple coupling sources threaten cascade collapse.

    A cascade is flagged when:
      - total_load > C_critical × cascade_load_fraction  (default 0.5)
      - AND Γ > Γ_max × gamma_fraction                   (default 0.875)

    This implements the Frame-Principle-Grenze analysis: Ρ → 0 when Γ → 1 - σ_Φ
    AND external coupling approaches C_critical.
    """

    def __init__(
        self,
        coupling: CouplingMatrix,
        cascade_load_fraction: float = 0.5,
        gamma_fraction: float = 0.875 / GAMMA_MAX,
    ) -> None:
        self.coupling = coupling
        self.cascade_load_fraction = cascade_load_fraction
        self._gamma_threshold = gamma_fraction * GAMMA_MAX

    def check(self, target_domain: str, gamma: float) -> CascadeEvent | None:
        """Return a CascadeEvent if cascade conditions are met, else None."""
        load = self.coupling.total_load(target_domain)
        if load <= self.coupling.c_critical * self.cascade_load_fraction:
            return None
        if gamma <= self._gamma_threshold:
            return None

        severity = "critical" if load >= self.coupling.c_critical else "warning"
        return CascadeEvent(
            target_domain=target_domain,
            gamma=gamma,
            total_coupling_load=load,
            active_sources=self.coupling.coupling_sources(target_domain),
            severity=severity,
        )

    def scan_all(
        self, domain_gamma: dict[str, float]
    ) -> list[CascadeEvent]:
        """Scan multiple domains and return all detected cascade events."""
        events = []
        for domain, gamma in domain_gamma.items():
            event = self.check(domain, gamma)
            if event is not None:
                events.append(event)
        return events
