"""Frame-Principle boundary analysis: σ_Φ ≈ 1/16.

Ρ → 0 as Γ → 1 - σ_Φ ≈ 0.9375 AND coupling load → C_critical.
This defines the inner boundary of the stability buffer.
"""

from __future__ import annotations

from resilience_core.constants import GAMMA_MAX, SIGMA_PHI


def frame_limit_gamma() -> float:
    """Return the Γ value at which the Frame-Principle boundary is reached.

    Defined as Γ_max · (1 - σ_Φ).  At this point the criticality margin
    approaches σ_Φ and Ρ collapses to zero when coupling load also peaks.
    """
    return GAMMA_MAX * (1.0 - SIGMA_PHI)


def within_frame_buffer(gamma: float, margin: float = SIGMA_PHI) -> bool:
    """True when Γ is still safely below the Frame-Principle boundary."""
    return gamma < frame_limit_gamma() - margin


def frame_principle_warning(rho: float) -> bool:
    """True when Ρ has crossed below the σ_Φ safety threshold."""
    return rho < SIGMA_PHI


def frame_principle_report(gamma: float, rho: float) -> dict[str, float | bool | str]:
    """Return a human-readable Frame-Principle status report."""
    limit = frame_limit_gamma()
    buffer_remaining = max(0.0, limit - gamma)
    warn = frame_principle_warning(rho)
    status = "critical" if warn else ("warning" if gamma > limit * 0.95 else "stable")
    return {
        "gamma": gamma,
        "rho": rho,
        "frame_limit_gamma": limit,
        "sigma_phi": SIGMA_PHI,
        "buffer_remaining": buffer_remaining,
        "within_buffer": within_frame_buffer(gamma),
        "frame_principle_warning": warn,
        "status": status,
    }
