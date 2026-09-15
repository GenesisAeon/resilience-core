"""Sandpile SOC calibration — Ρ_Sandpile reference value.

Sandpile: Γ = 0.296, Ρ_ref ≈ 0.75 (classically robust-critical).
λ*_Sandpile = r · tanh²(σ · 0.296) = 1.0 · tanh²(0.6512) ≈ 0.3277.

CALIBRATION TARGET: Ρ_Sandpile ≈ 0.75 (CREP-Atlas estimate).
  With r=1.0:  Ρ_Sandpile ≈ 0.2223  (r · 0.3277 · 0.6783)
  Required r for target: r ≈ 3.37  (= 0.75 / 0.2223)
  Status: OPEN — r to be determined from real sandpile/SOC coupling data
"""

from resilience_core import ResilienceCore

GAMMA_SANDPILE = 0.296
# With r=1.0; update to r~3.37 once sandpile/SOC coupling data is available.
RHO_SANDPILE_WITH_DEFAULT_R = 0.2223
RHO_SANDPILE_EXPECTED = 0.75        # CREP-Atlas target (requires calibrated r)
RHO_SANDPILE_TOLERANCE = 0.10
LAMBDA_STAR_EXPECTED = 0.3277   # r=1.0, tanh^2(2.2*0.296)
LAMBDA_STAR_TOLERANCE = 0.005
R_REQUIRED_FOR_TARGET = 3.37    # r needed to reach Ρ~0.75; pending real data


def run_sandpile_calibration() -> dict[str, object]:
    """Run sandpile calibration cycle and return verification dict."""
    core = ResilienceCore(domain="sandpile")
    core.run_cycle(gamma=GAMMA_SANDPILE)
    state = core.get_resilience_state()
    return {
        "domain": "sandpile",
        "gamma": GAMMA_SANDPILE,
        "rho": state["rho"],
        "rho_with_default_r": RHO_SANDPILE_WITH_DEFAULT_R,
        "rho_atlas_target": RHO_SANDPILE_EXPECTED,
        "r_required_for_target": R_REQUIRED_FOR_TARGET,
        "calibration_status": "OPEN — r to be determined from real sandpile/SOC coupling data",
        "lambda_star": state["lambda_star"],
        "recovery_time": state["recovery_time"],
        "lambda_in_range": abs(state["lambda_star"] - LAMBDA_STAR_EXPECTED) < LAMBDA_STAR_TOLERANCE,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_sandpile_calibration(), indent=2))
