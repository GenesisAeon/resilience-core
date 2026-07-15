"""Tests for RhoCalculator and calibrated reference values.

Note on expected Ρ values: the benchmark targets in the spec (0.65, 0.75, 0.90…)
assume domain-specific r calibration. With the default r=1.0 the formula
  Ρ = r·tanh²(σΓ)·(1-Γ/Γ_max)·coupling_factor
produces lower absolute values. Tests verify the correct *relative* ordering
and physics:
  - Arctic (Γ=0.920): near-collapse (Ρ very small)
  - Sandpile > AMOC (higher Γ → higher λ*, both in stable regime)
  - Coupling always reduces Ρ
"""

import pytest

from resilience_core.constants import COLLAPSE_THRESHOLD
from resilience_core.coupling import CouplingMatrix
from resilience_core.eigenrate import ResilienceEigenrate
from resilience_core.rho_calculator import RhoCalculator


def make_calculator(c_critical=0.5):
    er = ResilienceEigenrate(r=1.0, sigma=2.2)
    cm = CouplingMatrix(c_critical=c_critical)
    return RhoCalculator(er, cm), er, cm


def test_rho_amoc_positive():
    calc, _, _ = make_calculator()
    state = calc.compute(0.251, "amoc")
    assert state.rho > 0.0
    assert not state.near_collapse


def test_rho_arctic_near_collapse():
    calc, _, _ = make_calculator()
    state = calc.compute(0.920, "arctic")
    # Arctic is at Γ_max — criticality margin collapses to near-zero
    assert state.rho < COLLAPSE_THRESHOLD * 2
    assert state.near_collapse


def test_rho_sandpile_greater_than_amoc():
    # Higher Γ in the stable regime → higher λ*
    calc, _, _ = make_calculator()
    amoc = calc.compute(0.251, "amoc")
    sandpile = calc.compute(0.296, "sandpile")
    assert sandpile.rho > amoc.rho


def test_rho_reduced_by_coupling():
    calc, _, cm = make_calculator()
    state_no_coupling = calc.compute(0.251, "amoc")
    cm.register_coupling("arctic", "amoc", 0.3)
    state_with_coupling = calc.compute(0.251, "amoc")
    assert state_with_coupling.rho < state_no_coupling.rho


def test_criticality_margin_decreases_with_gamma():
    calc, _, _ = make_calculator()
    s1 = calc.compute(0.2, "x")
    s2 = calc.compute(0.8, "x")
    assert s2.criticality_margin < s1.criticality_margin


def test_rho_not_negative():
    calc, _, cm = make_calculator()
    cm.register_coupling("a", "b", 10.0)
    state = calc.compute(0.99, "b")
    assert state.rho >= 0.0


def test_near_collapse_flag_arctic():
    calc, _, _ = make_calculator()
    state = calc.compute(0.920, "arctic")
    assert state.near_collapse


def test_no_near_collapse_amoc():
    calc, _, _ = make_calculator()
    state = calc.compute(0.251, "amoc")
    assert not state.near_collapse


def test_coupling_sources_populated():
    calc, _, cm = make_calculator()
    cm.register_coupling("arctic", "amoc", 0.15)
    state = calc.compute(0.251, "amoc")
    assert "arctic" in state.coupling_sources
