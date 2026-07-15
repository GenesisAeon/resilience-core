"""UTAC fixpoint eigenrate λ*(t) = -r · tanh²(σΓ).

Pimm (1984) engineering resilience: τ_recovery ≈ 1/|λ*|.
λ* is always negative (stable attractor); we expose |λ*| throughout.
"""

from __future__ import annotations

import math

from resilience_core.constants import SIGMA


class ResilienceEigenrate:
    """Local return rate at the UTAC fixpoint.

    |λ*| measures resistance to *small* perturbations (Lyapunov-local).
    For large shocks / cascade thresholds see :class:`~resilience_core.coupling.CouplingMatrix`.
    """

    def __init__(self, r: float = 1.0, sigma: float = SIGMA) -> None:
        if r <= 0:
            raise ValueError(f"r must be positive, got {r}")
        if sigma <= 0:
            raise ValueError(f"sigma must be positive, got {sigma}")
        self.r = r
        self.sigma = sigma

    def compute(self, gamma: float) -> float:
        """Return |λ*| = r · tanh²(σΓ).

        Always ≥ 0. Returns 0 for invalid / NaN gamma.
        """
        if gamma is None or math.isnan(gamma):
            return 0.0
        gamma = max(0.0, float(gamma))
        return self.r * math.tanh(self.sigma * gamma) ** 2

    def recovery_time(self, gamma: float) -> float:
        """Return τ_recovery ≈ 1/|λ*| in system time units (∞ when λ*→0)."""
        lam = self.compute(gamma)
        return 1.0 / lam if lam > 1e-10 else math.inf
