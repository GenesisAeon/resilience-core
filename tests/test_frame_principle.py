"""Tests for Frame-Principle boundary analysis."""

import pytest

from resilience_core.constants import GAMMA_MAX, SIGMA_PHI
from resilience_core.frame_principle import (
    frame_limit_gamma,
    frame_principle_report,
    frame_principle_warning,
    within_frame_buffer,
)


def test_frame_limit_gamma_value():
    expected = GAMMA_MAX * (1.0 - SIGMA_PHI)
    assert frame_limit_gamma() == pytest.approx(expected)


def test_within_frame_buffer_safe():
    assert within_frame_buffer(0.5)


def test_within_frame_buffer_near_limit():
    # gamma approaching Γ_max should be outside buffer
    assert not within_frame_buffer(GAMMA_MAX * 0.95)


def test_frame_principle_warning_triggered():
    assert frame_principle_warning(rho=SIGMA_PHI - 0.001)


def test_frame_principle_warning_not_triggered():
    assert not frame_principle_warning(rho=0.5)


def test_report_stable():
    report = frame_principle_report(gamma=0.3, rho=0.65)
    assert report["status"] == "stable"
    assert not report["frame_principle_warning"]


def test_report_critical():
    report = frame_principle_report(gamma=0.9, rho=0.03)
    assert report["frame_principle_warning"]
    assert report["status"] in ("critical", "warning")
