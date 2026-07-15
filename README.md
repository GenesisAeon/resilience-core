# resilience-core — P40

**Domänenübergreifende Systemresilienzgröße Ρ**  
GenesisAeon Package 40 · MOR Research Collective · Johann Römer

[![CI](https://github.com/GenesisAeon/resilience-core/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/resilience-core/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## What is Ρ?

`resilience-core` implements the domain-overarching system resilience metric **Ρ** derived from UTAC (Universal Tipping Attractor Cascade) fixpoint analysis:

```
Ρ(t) = |λ*(t)| · (1 - Γ(t)/Γ_max) · (1 - Σ_j |C_ij(t)|/C_critical)
```

Three multiplicative factors:

| Factor | Meaning |
|--------|---------|
| `\|λ*\|` = r · tanh²(σΓ) | Intrinsic return rate to attractor (Pimm 1984 engineering resilience) |
| `1 - Γ/Γ_max` | Criticality margin — buffer before bifurcation |
| `1 - Σ\|C_ij\|/C_crit` | Coupling penalty — external destabilisation from other domains |

**Ρ → 0** when a system is simultaneously near its tipping point (Γ → Γ_max) AND receiving strong destabilising coupling (C_ij → C_critical). This formally captures **cascade collapse**.

---

## Installation

```bash
pip install resilience-core
# or
uv add resilience-core
```

## Quick Start

```python
from resilience_core import ResilienceCore, compute_rho

# Single domain
core = ResilienceCore(domain="amoc")
core.run_cycle(gamma=0.251)
print(core.get_resilience_state())
# {'rho': 0.654, 'lambda_star': 0.254, 'recovery_time': 3.94, ...}

# Convenience function
rho_arctic = compute_rho(gamma=0.920, domain="arctic")  # ≈ 0.05

# With inter-domain coupling
core_amoc = ResilienceCore(domain="amoc")
core_amoc.run_cycle(
    gamma=0.251,
    coupling_updates={("arctic_ice", "amoc"): 0.15, ("amazon", "amoc"): 0.08}
)
print(core_amoc.get_resilience_state()["rho"])  # < 0.65 (reduced by coupling)
```

## Calibrated Reference Values

| Domain | Γ | Ρ | Status |
|--------|---|---|--------|
| Quantum bit | 0.050 | ≈ 0.90 | Very resilient |
| Sandpile SOC | 0.296 | ≈ 0.75 | Classically robust |
| AMOC | 0.251 | ≈ 0.65 | Moderate, geologically perturbed |
| Arctic ERA5 | 0.920 | ≈ 0.05 | Near collapse |

## Diamond Interface

`ResilienceCore` implements all 6 GenesisAeon Diamond methods:

```python
core.run_cycle(gamma)         # Method 1: execute one step
core.get_crep_state()         # Method 2: CREP snapshot {C, R, E, P, Gamma}
core.get_utac_state()         # Method 3: UTAC snapshot {H, H_star, K_eff}
core.get_phase_events()       # Method 4: near-collapse & cascade events
core.to_zenodo_record()       # Method 5: Zenodo deposition metadata
core.get_resilience_state()   # Method 6 (NEW): full Ρ breakdown
```

`get_resilience_state()` is the **6th Diamond method** — a standard interface for all GenesisAeon packages to optionally expose via `resilience-core`.

## Frame-Principle Boundary

σ_Φ ≈ 1/16 = 0.0625 defines the collapse threshold:

```python
from resilience_core import frame_principle_report
report = frame_principle_report(gamma=0.9, rho=0.03)
# {'status': 'critical', 'frame_principle_warning': True, ...}
```

## Structure

```
resilience_core/
├── constants.py         # σ, σ_Φ, Γ_max, C_critical
├── eigenrate.py         # λ*(t) = -r·tanh²(σΓ)
├── coupling.py          # CouplingMatrix: C_ij inter-domain effects
├── cascade.py           # CascadeDetector: multi-domain collapse warning
├── rho_calculator.py    # RhoCalculator: Ρ = |λ*|·margin·coupling_factor
├── frame_principle.py   # σ_Φ boundary analysis
├── system.py            # ResilienceCore — Diamond Interface main class
└── benchmarks/          # Calibration scripts (AMOC, Arctic, Sandpile)
```

## Citation

```bibtex
@software{romer2026resiliencecore,
  author       = {Römer, Johann},
  title        = {resilience-core: UTAC-derived system resilience (Ρ)},
  year         = 2026,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://github.com/GenesisAeon/resilience-core}
}
```

---

Part of the [GenesisAeon](https://github.com/GenesisAeon) ecosystem · related: `diamond-setup` (P-INFRA-1), `scope-resilience` (P41)
