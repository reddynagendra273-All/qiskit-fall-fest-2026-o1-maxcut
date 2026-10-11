# NexGen Minds — QAOA Max-Cut

## Project Overview
This project explores the Quantum Approximate Optimization Algorithm (QAOA)
for solving the weighted Max-Cut problem and compares circuit-routing
metrics on illustrative connectivity architectures.

## Practice Graph
The graph contains five vertices: A, B, C, D, and E.

| Edge | Weight |
|---|---:|
| A-B | 3 |
| A-C | 2 |
| B-C | 1 |
| B-D | 4 |
| C-E | 2 |
| D-E | 3 |

The classical brute-force practice baseline found a maximum cut weight of 13.

## Experiments
- Classical Max-Cut baseline
- QAOA circuit construction and parameter exploration
- QAOA simulation validation
- Routing comparison using linear and ring connectivity
- Circuit depth, CX count, and gate-count analysis

## Recorded Practice Routing Results

| Metric | Linear | Ring |
|---|---:|---:|
| Circuit depth | 79 | 65 |
| Total gates | 163 | 136 |
| CX gates | 21 | 18 |
| Explicit SWAP gates | 0 | 0 |

These are simulator practice results using illustrative connectivity,
not official hackathon processor measurements.

**Important:** CX overhead is a proxy for routing cost, not an exact SWAP count.
A zero explicit SWAP count after transpilation does not prove that routing
introduced no overhead.

## Project Structure
- `src/` — Python scripts
- `data/raw/` — original input data
- `data/processed/` — processed data
- `results/tables/` — CSV metrics and text results
- `results/figures/` — generated plots
- `docs/` — documentation

## Setup
Use Python 3.11 or another Python version compatible with the installed
Qiskit dependencies.

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run commands from the project root:

```powershell
python src\maxcut_classical.py
python src\maxcut_qaoa.py
python src\optimize_qaoa.py
python src\validate_qaoa.py
python src\routing_analysis_v2.py
```

## Limitations
- Results are from practice simulations.
- The connectivity architectures are illustrative.
- Hardware execution and official processor benchmarking have not been claimed.
- Re-run experiments and record seeds, shots, and software versions for reproducibility.

## Team
NexGen Minds

## Status
Practice project; to be updated using the official challenge kit when available.
