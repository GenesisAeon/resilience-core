"""Sandpile SOC calibration — Ρ_Sandpile ≈ 0.75 (classically robust-critical).

Sandpile: Γ = 0.296, Ρ_ref ≈ 0.75.
"""

from resilience_core import ResilienceCore

GAMMA_SANDPILE = 0.296
RHO_SANDPILE_EXPECTED = 0.75
RHO_SANDPILE_TOLERANCE = 0.10


def run_sandpile_calibration() -> dict[str, object]:
    core = ResilienceCore(domain="sandpile")
    core.run_cycle(gamma=GAMMA_SANDPILE)
    state = core.get_resilience_state()
    return {
        "domain": "sandpile",
        "gamma": GAMMA_SANDPILE,
        "rho": state["rho"],
        "rho_in_range": abs(state["rho"] - RHO_SANDPILE_EXPECTED) < RHO_SANDPILE_TOLERANCE,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_sandpile_calibration(), indent=2))
