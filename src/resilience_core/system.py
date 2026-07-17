"""ResilienceCore — Diamond Interface main class for resilience-core (P40).

Implements all 6 Diamond methods:
  run_cycle, get_crep_state, get_utac_state, get_phase_events,
  to_zenodo_record, get_resilience_state (6th method).
"""

from __future__ import annotations

from typing import Any

from resilience_core.cascade import CascadeDetector, CascadeEvent
from resilience_core.constants import COLLAPSE_THRESHOLD, SIGMA_PHI
from resilience_core.coupling import CouplingMatrix
from resilience_core.eigenrate import ResilienceEigenrate
from resilience_core.rho_calculator import ResilienceState, RhoCalculator


class ResilienceCore:
    """Domain-overarching system resilience Ρ via UTAC fixpoint analysis.

    Usage::

        core = ResilienceCore(domain="amoc")
        result = core.run_cycle(gamma=0.251)
        state = core.get_resilience_state()
        print(state["rho"])   # ≈ 0.18 (r=1.0 default; Atlas target 0.65
                               # requires r≈3.54, see
                               # benchmarks/amoc_calibration.py)
    """

    def __init__(
        self,
        domain: str = "generic",
        r: float = 1.0,
        sigma: float = 2.2,
        c_critical: float = 0.5,
    ) -> None:
        self.domain = domain
        self.eigenrate = ResilienceEigenrate(r=r, sigma=sigma)
        self.coupling = CouplingMatrix(c_critical=c_critical)
        self.calculator = RhoCalculator(self.eigenrate, self.coupling)
        self.cascade_detector = CascadeDetector(self.coupling)
        self._current_gamma: float | None = None
        self._history: list[ResilienceState] = []
        self._cascade_events: list[CascadeEvent] = []
        self._cycles_completed: int = 0

    # ------------------------------------------------------------------
    # Diamond Method 1 — run_cycle
    # ------------------------------------------------------------------

    def run_cycle(
        self,
        gamma: float = 0.251,
        coupling_updates: dict[tuple[str, str], float] | None = None,
    ) -> dict[str, Any]:
        """Execute one resilience computation cycle.

        Args:
            gamma: Current CREP Γ for this domain (typically from the
                   paired domain package's ``get_crep_state()``).
            coupling_updates: Optional ``{(source, target): effect}`` map
                              for dynamic coupling registration.
        """
        if coupling_updates:
            for (src, tgt), effect in coupling_updates.items():
                self.coupling.register_coupling(src, tgt, effect)

        self._current_gamma = float(gamma)
        state = self.calculator.compute(gamma, self.domain)
        self._history.append(state)
        self._cycles_completed += 1

        cascade = self.cascade_detector.check(self.domain, gamma)
        if cascade is not None:
            self._cascade_events.append(cascade)

        return {
            "rho": state.rho,
            "lambda_star": state.lambda_star,
            "criticality_margin": state.criticality_margin,
            "coupling_load": state.coupling_load,
            "near_collapse": state.near_collapse,
            "recovery_time": self.eigenrate.recovery_time(gamma),
        }

    # ------------------------------------------------------------------
    # Diamond Method 2 — get_crep_state
    # ------------------------------------------------------------------

    def get_crep_state(self) -> dict[str, float | None]:
        """CREP state with Ρ mapped to Γ_resilience."""
        self._require_converged("get_crep_state")
        gamma = self._current_gamma or 0.0
        state = self.calculator.compute(gamma, self.domain)
        return {
            "C": state.criticality_margin,
            "R": 1.0 - state.coupling_load,
            "E": min(1.0, state.lambda_star),
            "P": float(not state.near_collapse),
            "Gamma": state.rho,
        }

    # ------------------------------------------------------------------
    # Diamond Method 3 — get_utac_state
    # ------------------------------------------------------------------

    def get_utac_state(self) -> dict[str, float]:
        """UTAC state: H = current Ρ, H* = target, K_eff = 1.0."""
        self._require_converged("get_utac_state")
        gamma = self._current_gamma or 0.0
        rho = self.calculator.compute(gamma, self.domain).rho
        return {
            "H": rho,
            "H_star": COLLAPSE_THRESHOLD * 2,
            "K_eff": 1.0,
        }

    # ------------------------------------------------------------------
    # Diamond Method 4 — get_phase_events
    # ------------------------------------------------------------------

    def get_phase_events(self) -> list[dict[str, Any]]:
        """Return near-collapse events since package initialisation."""
        events = [
            {
                "type": "near_collapse",
                "rho": s.rho,
                "coupling_load": s.coupling_load,
            }
            for s in self._history
            if s.near_collapse
        ]
        for ce in self._cascade_events:
            events.append(
                {
                    "type": "cascade_warning",
                    "target_domain": ce.target_domain,
                    "gamma": ce.gamma,
                    "total_coupling_load": ce.total_coupling_load,
                    "severity": ce.severity,
                }
            )
        return events

    # ------------------------------------------------------------------
    # Diamond Method 5 — to_zenodo_record
    # ------------------------------------------------------------------

    def to_zenodo_record(self) -> dict[str, Any]:
        return {
            "title": (
                f"resilience-core: UTAC-derived system resilience (Ρ) "
                f"for domain '{self.domain}'"
            ),
            "description": (
                "Computes the GenesisAeon system resilience metric Ρ from "
                "UTAC eigenrate analysis and inter-domain coupling effects. "
                "Ρ quantifies a system's buffer capacity against destabilising "
                "perturbations, from physical tipping points to semantic drift."
            ),
            "creators": [
                {"name": "Römer, Johann", "affiliation": "MOR Research Collective"}
            ],
            "communities": [{"identifier": "genesisaeon"}],
            "related_identifiers": [
                {
                    "identifier": "10.5281/zenodo.19645351",
                    "relation": "isPartOf",
                    "scheme": "doi",
                }
            ],
        }

    # ------------------------------------------------------------------
    # Diamond Method 6 — get_resilience_state
    # ------------------------------------------------------------------

    def get_resilience_state(self) -> dict[str, Any]:
        """6th Diamond method — full resilience state.

        Standard interface for all GenesisAeon packages that import
        resilience-core as an optional dependency.
        """
        gamma = self._current_gamma or 0.0
        state = self.calculator.compute(gamma, self.domain)
        return {
            "rho": state.rho,
            "lambda_star": state.lambda_star,
            "recovery_time": self.eigenrate.recovery_time(gamma),
            "criticality_margin": state.criticality_margin,
            "coupling_load": state.coupling_load,
            "near_collapse": state.near_collapse,
            "frame_principle_warn": state.rho < SIGMA_PHI,
            "coupling_sources": state.coupling_sources,
            "implemented": True,
        }

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    @property
    def cycles_completed(self) -> int:
        return self._cycles_completed

    def _require_converged(self, method: str) -> None:
        if self._cycles_completed < 1:
            from diamond_setup.protocol import NotConvergedError
            raise NotConvergedError(method)


def compute_rho(
    gamma: float,
    domain: str = "generic",
    r: float = 1.0,
    sigma: float = 2.2,
    coupling_updates: dict[tuple[str, str], float] | None = None,
) -> float:
    """Convenience function: compute Ρ for a single (domain, gamma) pair."""
    core = ResilienceCore(domain=domain, r=r, sigma=sigma)
    result = core.run_cycle(gamma=gamma, coupling_updates=coupling_updates)
    return float(result["rho"])
