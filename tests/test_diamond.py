"""Diamond Interface compliance tests for ResilienceCore."""

import pytest

from diamond_setup.protocol import NotConvergedError
from resilience_core.system import ResilienceCore


@pytest.fixture
def core():
    return ResilienceCore(domain="amoc")


def test_not_converged_raises_before_run_cycle(core):
    with pytest.raises(NotConvergedError):
        core.get_crep_state()

    with pytest.raises(NotConvergedError):
        core.get_utac_state()


def test_run_cycle_returns_dict(core):
    result = core.run_cycle(gamma=0.251)
    assert isinstance(result, dict)
    assert "rho" in result


def test_crep_state_keys(core):
    core.run_cycle(gamma=0.251)
    crep = core.get_crep_state()
    for key in ("C", "R", "E", "P", "Gamma"):
        assert key in crep, f"Missing key: {key}"


def test_crep_gamma_not_none_after_run(core):
    core.run_cycle(gamma=0.251)
    assert core.get_crep_state()["Gamma"] is not None


def test_crep_gamma_in_range(core):
    core.run_cycle(gamma=0.251)
    gamma = core.get_crep_state()["Gamma"]
    assert 0.0 <= gamma <= 1.0


def test_utac_state_keys(core):
    core.run_cycle(gamma=0.251)
    utac = core.get_utac_state()
    for key in ("H", "H_star", "K_eff"):
        assert key in utac, f"Missing key: {key}"


def test_phase_events_is_list(core):
    core.run_cycle(gamma=0.251)
    assert isinstance(core.get_phase_events(), list)


def test_zenodo_record_keys(core):
    zr = core.to_zenodo_record()
    for key in ("title", "description", "creators"):
        assert key in zr


def test_resilience_state_rho(core):
    core.run_cycle(gamma=0.251)
    state = core.get_resilience_state()
    assert "rho" in state
    assert state["implemented"] is True
    assert 0.0 <= state["rho"] <= 1.0


def test_cycles_completed_increments(core):
    assert core.cycles_completed == 0
    core.run_cycle(gamma=0.251)
    assert core.cycles_completed == 1
    core.run_cycle(gamma=0.300)
    assert core.cycles_completed == 2


def test_near_collapse_arctic():
    core = ResilienceCore(domain="arctic")
    core.run_cycle(gamma=0.920)
    state = core.get_resilience_state()
    assert state["near_collapse"]
    assert state["frame_principle_warn"]


def test_coupling_updates_via_run_cycle():
    core = ResilienceCore(domain="amoc")
    result_no_coupling = core.run_cycle(gamma=0.251)
    core2 = ResilienceCore(domain="amoc")
    result_with_coupling = core2.run_cycle(
        gamma=0.251,
        coupling_updates={("arctic", "amoc"): 0.3},
    )
    assert result_with_coupling["rho"] < result_no_coupling["rho"]


def test_compute_rho_convenience():
    from resilience_core.system import compute_rho
    rho = compute_rho(gamma=0.251, domain="amoc")
    assert 0.0 < rho < 1.0
