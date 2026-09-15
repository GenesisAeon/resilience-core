"""Tests for CREP-Atlas calibration runners (honesty / OPEN status).

Does not assert that default-r rho hits atlas targets — those require
domain-specific r calibration (see amoc/arctic/sandpile calibration modules).
"""

from resilience_core.benchmarks.amoc_calibration import run_amoc_calibration
from resilience_core.benchmarks.arctic_calibration import run_arctic_calibration
from resilience_core.benchmarks.sandpile_calibration import run_sandpile_calibration


def test_amoc_calibration_status_open():
    result = run_amoc_calibration()
    assert "calibration_status" in result
    assert str(result["calibration_status"]).startswith("OPEN")


def test_arctic_calibration_status_open():
    result = run_arctic_calibration()
    assert "calibration_status" in result
    assert str(result["calibration_status"]).startswith("OPEN")
    assert "r_required_for_target" not in result


def test_sandpile_calibration_status_open():
    result = run_sandpile_calibration()
    assert "calibration_status" in result
    assert str(result["calibration_status"]).startswith("OPEN")
    assert "r_required_for_target" in result


def test_all_calibration_runners_return_status():
    for runner in (run_amoc_calibration, run_arctic_calibration, run_sandpile_calibration):
        result = runner()
        assert isinstance(result, dict)
        assert "calibration_status" in result
