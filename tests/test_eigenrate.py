"""Tests for ResilienceEigenrate."""

import math

import pytest

from resilience_core.eigenrate import ResilienceEigenrate


def test_lambda_star_positive():
    er = ResilienceEigenrate()
    assert er.compute(0.251) > 0


def test_lambda_star_zero_at_zero_gamma():
    er = ResilienceEigenrate()
    assert er.compute(0.0) == pytest.approx(0.0)


def test_lambda_star_amoc():
    er = ResilienceEigenrate(r=1.0, sigma=2.2)
    lam = er.compute(0.251)
    # tanh(2.2 * 0.251) = tanh(0.5522) ≈ 0.5039 → lam ≈ 0.254
    assert lam == pytest.approx(math.tanh(2.2 * 0.251) ** 2, rel=1e-6)


def test_lambda_star_increases_with_gamma():
    er = ResilienceEigenrate()
    assert er.compute(0.5) > er.compute(0.2)


def test_lambda_star_nan_returns_zero():
    er = ResilienceEigenrate()
    assert er.compute(float("nan")) == 0.0


def test_recovery_time_finite():
    er = ResilienceEigenrate()
    rt = er.recovery_time(0.251)
    assert rt > 0 and math.isfinite(rt)


def test_recovery_time_infinite_at_zero():
    er = ResilienceEigenrate()
    assert er.recovery_time(0.0) == math.inf


def test_invalid_r_raises():
    with pytest.raises(ValueError):
        ResilienceEigenrate(r=-1.0)


def test_invalid_sigma_raises():
    with pytest.raises(ValueError):
        ResilienceEigenrate(sigma=0.0)
