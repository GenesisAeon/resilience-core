"""AMOC calibration — Ρ_AMOC reference value.

AMOC: Γ = 0.251, Ρ_ref ≈ 0.65 (moderate resilience, geologically perturbed).
λ*_AMOC = r · tanh²(σ · 0.251) = 1.0 · tanh²(0.552) ≈ 0.269.
"""

from resilience_core import ResilienceCore


GAMMA_AMOC = 0.251
RHO_AMOC_EXPECTED = 0.65
RHO_AMOC_TOLERANCE = 0.10
LAMBDA_STAR_EXPECTED = 0.269
LAMBDA_STAR_TOLERANCE = 0.05


def run_amoc_calibration() -> dict:
    """Run AMOC calibration cycle and return verification dict."""
    core = ResilienceCore(domain="amoc")
    result = core.run_cycle(gamma=GAMMA_AMOC)
    state = core.get_resilience_state()
    return {
        "domain": "amoc",
        "gamma": GAMMA_AMOC,
        "rho": state["rho"],
        "lambda_star": state["lambda_star"],
        "recovery_time": state["recovery_time"],
        "rho_in_range": abs(state["rho"] - RHO_AMOC_EXPECTED) < RHO_AMOC_TOLERANCE,
        "lambda_in_range": abs(state["lambda_star"] - LAMBDA_STAR_EXPECTED) < LAMBDA_STAR_TOLERANCE,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_amoc_calibration(), indent=2))
