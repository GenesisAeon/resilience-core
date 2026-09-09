"""Algebraic connectivity of the inter-domain coupling graph.

Ρ (rho_calculator.py) and cascade detection (cascade.py) analyse coupling
*load* — how much destabilising pressure converges on one domain. Neither
detects a structurally different failure mode: a coupling *topology* that
is only weakly connected, or fragmenting into isolated dense clusters, even
when no single domain looks critical in isolation. Densely-clustered,
weakly-inter-connected sub-groups can trap and amplify a local perturbation
(e.g. semantic drift, a hallucination cascade in a multi-agent network)
without it ever propagating to the rest of the network, where consensus or
correction could occur.

The algebraic connectivity (the second-smallest eigenvalue of the graph
Laplacian, the "Fiedler value") is the standard spectral-graph-theory
measure for this: it is exactly zero iff the graph is disconnected, and
low-but-positive values indicate a near-bottleneck — one or few edges whose
removal would fragment the network.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from resilience_core.coupling import CouplingMatrix


class NetworkConnectivity:
    """Computes spectral connectivity diagnostics for a CouplingMatrix's graph.

    The coupling registry is directed (C_ij != C_ji in general — see
    ``coupling.py``), but algebraic connectivity is defined for undirected
    graphs. This class symmetrises each registered coupling into a single
    undirected edge with weight ``|effect_ij| + |effect_ji|`` (0 if only one
    direction is registered), since both directions represent *some*
    structural link between the domains regardless of sign or direction.
    """

    def __init__(self, coupling: CouplingMatrix) -> None:
        self.coupling = coupling

    def _domains(self) -> list[str]:
        domains: set[str] = set()
        for src, tgt in self.coupling.all_couplings():
            domains.add(src)
            domains.add(tgt)
        return sorted(domains)

    def adjacency_matrix(self) -> tuple[npt.NDArray[np.float64], list[str]]:
        """Return (W, domains): symmetric non-negative weighted adjacency matrix.

        ``domains[i]`` names the domain represented by row/column *i* of *W*.
        """
        domains = self._domains()
        index = {d: i for i, d in enumerate(domains)}
        n = len(domains)
        w = np.zeros((n, n))
        for (src, tgt), effect in self.coupling.all_couplings().items():
            i, j = index[src], index[tgt]
            if i == j:
                continue
            w[i, j] += abs(effect)
            w[j, i] += abs(effect)
        return w, domains

    def laplacian(self) -> tuple[npt.NDArray[np.float64], list[str]]:
        """Return (L, domains) where L = D - W is the combinatorial graph Laplacian."""
        w, domains = self.adjacency_matrix()
        degree = np.diag(w.sum(axis=1))
        return degree - w, domains

    def algebraic_connectivity(self) -> float:
        """Return the Fiedler value (second-smallest Laplacian eigenvalue).

        Returns 0.0 for fewer than 2 domains (no meaningful connectivity to
        measure) and for graphs that are actually disconnected — both cases
        genuinely have zero algebraic connectivity by the standard
        definition, not a computational shortfall.
        """
        n_domains = len(self._domains())
        if n_domains < 2:
            return 0.0
        laplacian, _ = self.laplacian()
        eigenvalues = np.linalg.eigvalsh(laplacian)
        return float(max(0.0, eigenvalues[1]))

    def is_fragmentation_risk(self, threshold: float = 0.1) -> bool:
        """True when algebraic connectivity is at or below *threshold*.

        ``threshold`` is an uncalibrated default (no CREP Atlas reference
        value exists for this metric yet, unlike Γ/Ρ) — treat it as a
        conservative starting point, not a validated cutoff.
        """
        return self.algebraic_connectivity() <= threshold
