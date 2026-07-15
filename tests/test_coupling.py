"""Tests for CouplingMatrix."""

import pytest

from resilience_core.coupling import CouplingMatrix


def test_empty_load_is_zero():
    cm = CouplingMatrix()
    assert cm.total_load("amoc") == 0.0


def test_register_and_load():
    cm = CouplingMatrix(c_critical=0.5)
    cm.register_coupling("arctic", "amoc", effect=0.15)
    assert cm.total_load("amoc") == pytest.approx(0.15)


def test_coupling_factor_full():
    cm = CouplingMatrix(c_critical=0.5)
    cm.register_coupling("arctic", "amoc", effect=0.5)
    assert cm.coupling_factor("amoc") == pytest.approx(0.0)


def test_coupling_factor_no_coupling():
    cm = CouplingMatrix(c_critical=0.5)
    assert cm.coupling_factor("amoc") == pytest.approx(1.0)


def test_multiple_sources_sum():
    cm = CouplingMatrix(c_critical=0.5)
    cm.register_coupling("arctic", "amoc", 0.10)
    cm.register_coupling("amazon", "amoc", 0.08)
    assert cm.total_load("amoc") == pytest.approx(0.18)


def test_cascade_threshold_not_triggered():
    cm = CouplingMatrix()
    assert not cm.cascade_threshold("amoc", gamma=0.251)


def test_cascade_threshold_triggered():
    cm = CouplingMatrix(c_critical=0.5)
    cm.register_coupling("arctic", "amoc", 0.30)
    # gamma must be > 0.920 * 0.95 = 0.874
    assert cm.cascade_threshold("amoc", gamma=0.90)


def test_remove_coupling():
    cm = CouplingMatrix()
    cm.register_coupling("arctic", "amoc", 0.15)
    cm.remove_coupling("arctic", "amoc")
    assert cm.total_load("amoc") == 0.0


def test_coupling_sources():
    cm = CouplingMatrix()
    cm.register_coupling("arctic", "amoc", 0.10)
    cm.register_coupling("amazon", "amoc", 0.08)
    sources = cm.coupling_sources("amoc")
    assert sources == {"arctic": 0.10, "amazon": 0.08}
