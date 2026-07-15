"""resilience-core — domänenübergreifende Systemresilienzgröße Ρ (P40).

Quick start::

    from resilience_core import ResilienceCore, compute_rho

    core = ResilienceCore(domain="amoc")
    core.run_cycle(gamma=0.251)
    print(core.get_resilience_state())

    rho = compute_rho(gamma=0.920, domain="arctic")  # ≈ 0.05
"""

from resilience_core.cascade import CascadeDetector, CascadeEvent
from resilience_core.constants import (
    BENCHMARK_GAMMA,
    BENCHMARK_RHO,
    C_CRITICAL,
    COLLAPSE_THRESHOLD,
    GAMMA_MAX,
    SIGMA,
    SIGMA_PHI,
)
from resilience_core.coupling import CouplingMatrix
from resilience_core.eigenrate import ResilienceEigenrate
from resilience_core.frame_principle import (
    frame_limit_gamma,
    frame_principle_report,
    frame_principle_warning,
    within_frame_buffer,
)
from resilience_core.rho_calculator import ResilienceState, RhoCalculator
from resilience_core.system import ResilienceCore, compute_rho

__version__ = "1.0.0"
__all__ = [
    "ResilienceCore",
    "compute_rho",
    "ResilienceEigenrate",
    "CouplingMatrix",
    "RhoCalculator",
    "ResilienceState",
    "CascadeDetector",
    "CascadeEvent",
    "frame_limit_gamma",
    "frame_principle_report",
    "frame_principle_warning",
    "within_frame_buffer",
    "SIGMA",
    "SIGMA_PHI",
    "GAMMA_MAX",
    "C_CRITICAL",
    "COLLAPSE_THRESHOLD",
    "BENCHMARK_GAMMA",
    "BENCHMARK_RHO",
]
