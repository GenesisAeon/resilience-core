"""AMOC calibration — Ρ_AMOC reference value.

AMOC: Γ = 0.251, Ρ_ref ≈ 0.65 (moderate resilience, geologically perturbed).
λ*_AMOC = r · tanh²(σ · 0.251) = 1.0 · tanh²(0.552) ≈ 0.2522.

CALIBRATION TARGET: Ρ_AMOC ≈ 0.65 (CREP-Atlas estimate, from AMOC observational
  coherence data; not a direct measurement).
  With r=1.0:  Ρ_AMOC ≈ 0.1834  (r · 0.2522 · 0.7272)
  Required r for target: r ≈ 3.54  (= 0.65 / 0.1834)
  Status: OPEN — r to be determined from real AMOC timeseries coupling data
  Source: amoc-utac (P18) will supply dH/dt observations for r calibration.
"""

from resilience_core import ResilienceCore

GAMMA_AMOC = 0.251
# With r=1.0; update to r≈3.54 once amoc-utac timeseries data is available.
RHO_AMOC_WITH_DEFAULT_R = 0.1834
RHO_AMOC_EXPECTED = 0.65        # CREP-Atlas target (requires calibrated r)
RHO_AMOC_TOLERANCE = 0.10
LAMBDA_STAR_EXPECTED = 0.2522   # r=1.0, tanh²(2.2·0.251)
LAMBDA_STAR_TOLERANCE = 0.005
R_REQUIRED_FOR_TARGET = 3.54    # r needed to reach Ρ≈0.65; pending real data


def run_amoc_calibration() -> dict:
    """Run AMOC calibration cycle and return verification dict."""
    core = ResilienceCore(domain="amoc")
    core.run_cycle(gamma=GAMMA_AMOC)
    state = core.get_resilience_state()
    return {
        "domain": "amoc",
        "gamma": GAMMA_AMOC,
        "rho": state["rho"],
        "rho_with_default_r": RHO_AMOC_WITH_DEFAULT_R,
        "rho_atlas_target": RHO_AMOC_EXPECTED,
        "r_required_for_target": R_REQUIRED_FOR_TARGET,
        "calibration_status": "OPEN — pending amoc-utac (P18) timeseries",
        "lambda_star": state["lambda_star"],
        "recovery_time": state["recovery_time"],
        "lambda_in_range": abs(state["lambda_star"] - LAMBDA_STAR_EXPECTED) < LAMBDA_STAR_TOLERANCE,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_amoc_calibration(), indent=2))
