# NexGen Minds | QAOA Max-Cut Optimization

**Qiskit Fall Fest SRMAP 2026 — PS-O1: Max-Cut on Weighted Graphs**

## Project Overview

This project explores the Quantum Approximate Optimization Algorithm (QAOA) for weighted Max-Cut problems and investigates how processor connectivity affects quantum-circuit transpilation.

**Project status:** Practice simulations and ideal transpilation experiments. No actual quantum hardware measurements are claimed.

## Objectives

* Compute exact classical Max-Cut solutions using brute force.
* Construct and simulate p=1 QAOA circuits.
* Search for promising QAOA parameters using a coarse grid.
* Compare the feasibility and transpilation metrics of Processor A and Processor B.
* Analyze circuit depth, total gate count, CX count, and explicit SWAP count.
* Document limitations and identify future noise-aware experiments.

## Dataset and Classical Results

The dataset contains three team-created weighted graphs, each with six vertices and integer edge weights. These are practice instances, not official fixed benchmark instances.

| Graph    | Classical optimum | Optimal assignments | Assignments checked |
| -------- | ----------------: | ------------------: | ------------------: |
| graph_01 |                26 |                   2 |                  64 |
| graph_02 |                27 |                   2 |                  64 |
| graph_03 |                24 |                   4 |                  64 |

Graph definitions are stored in `data/raw/maxcut_instances.json`. Exact classical results are stored in `results/tables/classical_optima.csv`.

The classical optimum is the maximum total weight of edges crossing between the two vertex groups.

## QAOA Parameter Search

The parameter-grid search evaluates 32 combinations per graph using 4,096 shots. The selected parameters are the best candidates within the tested grid, chosen by average cut weight. They are not guaranteed to be globally optimal.

| Graph    | Gamma | Beta | Classical optimum | Best sampled cut | Average cut weight | Average approximation ratio | Best sampled ratio | Optimal-cut probability |
| -------- | ----: | ---: | ----------------: | ---------------: | -----------------: | --------------------------: | -----------------: | ----------------------: |
| graph_01 |   0.1 |  0.3 |                26 |               26 |            19.3484 |                      0.7442 |             1.0000 |                0.131592 |
| graph_02 |   0.1 |  0.3 |                27 |               27 |            19.1550 |                      0.7094 |             1.0000 |                0.133789 |
| graph_03 |   0.1 |  0.3 |                24 |               24 |            19.2749 |                      0.8031 |             1.0000 |                0.194092 |

The average approximation ratio is the average sampled cut weight divided by the exact classical optimum. The best sampled approximation ratio refers to the highest cut weight observed in the samples; it is not the average ratio.

Detailed results are stored in `results/tables/qaoa_optimization.csv`. Fixed-parameter simulation results are stored in `results/tables/qaoa_dataset_results.csv`.

These results describe simulator experiments, not hardware performance.

## Processor Architectures

Processor definitions are stored in `processors/processor_A.json` and `processors/processor_B.json`.

### Processor A

* Physical qubits: 5
* Coupling edges: (0,1), (1,2), (2,3), (3,4)
* Direct one-to-one mapping of all six logical qubits is infeasible because only five physical qubits are available.

### Processor B

* Physical qubits: 9
* Coupling edges: (0,1), (1,2), (2,3), (2,4), (4,5), (5,6), (4,7), (7,8)
* A direct mapping is feasible by qubit count. This does not, by itself, prove that every circuit interaction can be implemented without routing overhead.

### Processor B Transpilation Results

| Graph    | Circuit depth | Total gates | CX count | Explicit SWAP count |
| -------- | ------------: | ----------: | -------: | ------------------: |
| graph_01 |           123 |         218 |       41 |                   0 |
| graph_02 |           124 |         213 |       38 |                   0 |
| graph_03 |           139 |         270 |       47 |                   0 |

These metrics are from the current ideal transpilation setup. They are not quantum hardware measurements.

An explicit SWAP count of zero does not prove that routing added no overhead. Routing and gate decomposition can affect depth and gate counts without leaving explicit SWAP instructions in the final circuit.

The processor comparison is stored in `results/tables/processor_routing_comparison.csv`. Consolidated results are stored in `results/tables/consolidated_benchmark.csv`.

**Noise-model status:** Processor noise parameters have not yet been verified as implemented in this repository. Do not interpret the results above as noise-aware benchmark results.

## Figures

* `results/figures/maxcut_graph.png` — visualization of a practice Max-Cut graph.
* `results/figures/qaoa_approximation_ratios.png` — comparison of QAOA approximation ratios.
* `results/figures/processor_b_circuit_cost.png` — comparison of Processor B circuit-cost metrics.

## Project Structure

```text
maxcut-practice/
├── data/
│   └── raw/
│       └── maxcut_instances.json
├── processors/
│   ├── processor_A.json
│   └── processor_B.json
├── results/
│   ├── figures/
│   └── tables/
├── src/
│   ├── maxcut_classical.py
│   ├── maxcut_qaoa.py
│   ├── optimize_dataset_qaoa.py
│   ├── qaoa_dataset_benchmark.py
│   ├── processor_routing_benchmark.py
│   ├── consolidate_results.py
│   └── plot_benchmark_results.py
├── requirements.txt
├── requirements-lock.txt
└── README.md
```

Additional practice scripts and result files are included in `src/` and `results/`.

## Requirements

The working environment used for the latest experiments includes:

* Python 3.14.7
* Qiskit 2.5.2
* Qiskit Aer 0.17.2
* NumPy
* Matplotlib
* NetworkX

Dependency specifications are provided in `requirements.txt` and `requirements-lock.txt`. Results may vary with software versions, random seeds, circuit construction, and simulator settings.

## Installation

Run these commands from PowerShell:

```powershell
git clone https://github.com/reddynagendra273-All/qiskit-fall-fest-2026-o1-maxcut.git
cd qiskit-fall-fest-2026-o1-maxcut

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If the virtual environment already exists, activate it rather than creating another one.

## Running the Dataset Experiments

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe src\maxcut_classical.py
.\.venv\Scripts\python.exe src\qaoa_dataset_benchmark.py
.\.venv\Scripts\python.exe src\optimize_dataset_qaoa.py
.\.venv\Scripts\python.exe src\processor_routing_benchmark.py
.\.venv\Scripts\python.exe src\consolidate_results.py
.\.venv\Scripts\python.exe src\plot_benchmark_results.py
```

Review regenerated outputs before committing them. Older scripts may run separate illustrative experiments and should not be mixed with the six-vertex benchmark unless their differences are documented.

## Limitations and Future Work

* The three graphs are team-created practice inputs, not official fixed benchmark instances.
* The parameter search is a coarse grid and does not guarantee globally optimal parameters.
* Processor A cannot directly map all six logical qubits onto five physical qubits using a one-to-one mapping.
* Transpilation metrics are not hardware results.
* A zero explicit SWAP count does not establish zero routing overhead.
* Processor noise parameters and noise-aware results require implementation and verification.
* A reproducible notebook, final technical report, and clean-environment reproduction test remain to be completed if required by the organizer's submission checklist.
* Processor D requirements must be checked against the official challenge materials before finalizing the architecture design.

## Team Information

**Team:** NexGen Minds
**Challenge:** Qiskit Fall Fest SRMAP 2026 — PS-O1: Max-Cut on Weighted Graphs
