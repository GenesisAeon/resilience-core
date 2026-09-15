"""Arctic ERA5 calibration — Ρ_Arctic reference value.

Arctic: Γ = 0.920, Ρ_ref ≈ 0.05 (near-collapse reference).
λ*_Arctic = r · tanh²(σ · 0.920) = 1.0 · tanh²(2.024) ≈ 0.9325.

CALIBRATION TARGET: Ρ_Arctic ≈ 0.05 (CREP-Atlas estimate).
  With r=1.0:  Ρ_Arctic = 0.0  (criticality_margin = 1 - Γ/Γ_max = 0)
  Required r for target: UNDEFINED — Γ_max equals this domain's own benchmark
    Γ, so criticality_margin is structurally zero for any finite r (coupling_factor=1).
  Status: OPEN — structural circularity; see constants.py Known-Issue on GAMMA_MAX
  Note: atlas target Ρ≈0.05 cannot be reached by raising r alone while
    GAMMA_MAX == GAMMA_ARCTIC.
"""

from resilience_core import ResilienceCore

GAMMA_ARCTIC = 0.920
# With r=1.0; rho is identically 0 because criticality_margin is structurally zero.
RHO_ARCTIC_WITH_DEFAULT_R = 0.0
RHO_ARCTIC_EXPECTED = 0.05        # CREP-Atlas target (unreachable via r while Gamma=Gamma_max)
RHO_ARCTIC_TOLERANCE = 0.02
LAMBDA_STAR_EXPECTED = 0.9325   # r=1.0, tanh^2(2.2*0.920)
LAMBDA_STAR_TOLERANCE = 0.005
# R_REQUIRED_FOR_TARGET intentionally omitted — undefined (division by zero margin)


def run_arctic_calibration() -> dict[str, object]:
    """Run Arctic calibration cycle and return verification dict."""
    core = ResilienceCore(domain="arctic_era5")
    core.run_cycle(gamma=GAMMA_ARCTIC)
    state = core.get_resilience_state()
    return {
        "domain": "arctic_era5",
        "gamma": GAMMA_ARCTIC,
        "rho": state["rho"],
        "rho_with_default_r": RHO_ARCTIC_WITH_DEFAULT_R,
        "rho_atlas_target": RHO_ARCTIC_EXPECTED,
        "calibration_status": (
            "OPEN — GAMMA_MAX equals this domain's own benchmark Gamma so "
            "criticality_margin is structurally zero; see constants.py"
        ),
        "lambda_star": state["lambda_star"],
        "recovery_time": state["recovery_time"],
        "near_collapse": state["near_collapse"],
        "frame_principle_warn": state["frame_principle_warn"],
        "lambda_in_range": abs(state["lambda_star"] - LAMBDA_STAR_EXPECTED) < LAMBDA_STAR_TOLERANCE,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_arctic_calibration(), indent=2))
