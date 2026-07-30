"""Tests for NetworkConnectivity."""

import pytest

from resilience_core.coupling import CouplingMatrix
from resilience_core.graph_connectivity import NetworkConnectivity


def test_no_domains_has_zero_connectivity():
    nc = NetworkConnectivity(CouplingMatrix())
    assert nc.algebraic_connectivity() == 0.0


def test_single_edge_two_domains():
    cm = CouplingMatrix()
    cm.register_coupling("arctic", "amoc", effect=0.15)
    nc = NetworkConnectivity(cm)
    w, domains = nc.adjacency_matrix()
    assert domains == ["amoc", "arctic"]
    assert w[0, 1] == pytest.approx(0.15)
    assert w[1, 0] == pytest.approx(0.15)


def test_two_domain_chain_has_positive_connectivity():
    cm = CouplingMatrix()
    cm.register_coupling("arctic", "amoc", effect=0.15)
    nc = NetworkConnectivity(cm)
    # For a 2-node graph with edge weight w, Laplacian eigenvalues are 0 and 2w.
    assert nc.algebraic_connectivity() == pytest.approx(0.30)


def test_bidirectional_coupling_sums_weight():
    cm = CouplingMatrix()
    cm.register_coupling("arctic", "amoc", effect=0.10)
    cm.register_coupling("amoc", "arctic", effect=0.05)
    nc = NetworkConnectivity(cm)
    w, _ = nc.adjacency_matrix()
    assert w[0, 1] == pytest.approx(0.15)


def test_disconnected_components_have_zero_connectivity():
    cm = CouplingMatrix()
    cm.register_coupling("arctic", "amoc", effect=0.15)
    cm.register_coupling("sandpile", "quantum", effect=0.20)
    nc = NetworkConnectivity(cm)
    assert nc.algebraic_connectivity() == pytest.approx(0.0, abs=1e-9)


def test_negative_effect_uses_absolute_value():
    cm = CouplingMatrix()
    cm.register_coupling("deep_water", "amoc", effect=-0.30)
    nc = NetworkConnectivity(cm)
    assert nc.algebraic_connectivity() == pytest.approx(0.60)


def test_fragmentation_risk_flags_weak_bottleneck():
    cm = CouplingMatrix()
    cm.register_coupling("arctic", "amoc", effect=0.02)
    nc = NetworkConnectivity(cm)
    assert nc.is_fragmentation_risk(threshold=0.1)


def test_fragmentation_risk_false_for_strong_link():
    cm = CouplingMatrix()
    cm.register_coupling("arctic", "amoc", effect=0.50)
    nc = NetworkConnectivity(cm)
    assert not nc.is_fragmentation_risk(threshold=0.1)


def test_well_connected_triangle_has_higher_connectivity_than_chain():
    chain = CouplingMatrix()
    chain.register_coupling("a", "b", effect=0.2)
    chain.register_coupling("b", "c", effect=0.2)

    triangle = CouplingMatrix()
    triangle.register_coupling("a", "b", effect=0.2)
    triangle.register_coupling("b", "c", effect=0.2)
    triangle.register_coupling("a", "c", effect=0.2)

    chain_conn = NetworkConnectivity(chain).algebraic_connectivity()
    triangle_conn = NetworkConnectivity(triangle).algebraic_connectivity()
    assert triangle_conn > chain_conn
