"""Arctic ERA5 calibration — Ρ_Arctic ≈ 0.05 (near-collapse reference).

Arctic: Γ = 0.920, Ρ_ref ≈ 0.05.
Recovery time: τ ≈ 1/|λ*| ≈ 20 system-time units (extremely slow).
"""

from resilience_core import ResilienceCore

GAMMA_ARCTIC = 0.920
RHO_ARCTIC_EXPECTED = 0.05
RHO_ARCTIC_TOLERANCE = 0.02
RECOVERY_TIME_EXPECTED = 20.0
RECOVERY_TIME_TOLERANCE = 5.0


def run_arctic_calibration() -> dict[str, object]:
    """Run Arctic calibration cycle and return verification dict."""
    core = ResilienceCore(domain="arctic_era5")
    core.run_cycle(gamma=GAMMA_ARCTIC)
    state = core.get_resilience_state()
    return {
        "domain": "arctic_era5",
        "gamma": GAMMA_ARCTIC,
        "rho": state["rho"],
        "near_collapse": state["near_collapse"],
        "frame_principle_warn": state["frame_principle_warn"],
        "recovery_time": state["recovery_time"],
        "rho_in_range": abs(state["rho"] - RHO_ARCTIC_EXPECTED) < RHO_ARCTIC_TOLERANCE,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_arctic_calibration(), indent=2))
