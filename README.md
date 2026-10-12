# NexGen Minds | QAOA Max-Cut Optimization

**Qiskit Fall Fest SRMAP 2026 — PS-O1: Max-Cut on Weighted Graphs**

## Project Overview

This project explores the Quantum Approximate Optimization Algorithm (QAOA) for weighted Max-Cut problems. It investigates how processor connectivity affects circuit transpilation and evaluates a proposed workload-aware processor architecture using ideal transpilation metrics and noisy quantum-circuit simulation.

**Project status:** Classical reference calculations, QAOA simulations, ideal transpilation experiments, and noisy Aer simulations have been performed. No actual quantum hardware measurements are claimed.

## Objectives

* Compute exact classical Max-Cut solutions using brute force.
* Construct and simulate p=1 QAOA circuits.
* Search for promising QAOA parameters using a coarse grid.
* Compare processor feasibility and transpilation metrics.
* Analyze circuit depth, total gate count, CX count, and explicit SWAP count.
* Evaluate noisy simulation results using a consistent gate-noise model.
* Investigate a proposed workload-aware architecture, Processor D.
* Document limitations and provide reproducible experiment scripts.

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
| graph_02 |   0.1 |  0.3 |                27 |               27 |            19.1550 |                      0.7094 |            0.7094* |                0.133789 |
| graph_03 |   0.1 |  0.3 |                24 |               24 |            19.2749 |                      0.8031 |             1.0000 |                0.194092 |

*Verify the graph_02 best sampled ratio against the original result file before final submission; the previously recorded value should not be silently changed.

The average approximation ratio is the average sampled cut weight divided by the exact classical optimum. The best sampled approximation ratio refers to the highest cut weight observed in the samples; it is not the average ratio.

Detailed results are stored in `results/tables/qaoa_optimization.csv`. Fixed-parameter simulation results are stored in `results/tables/qaoa_dataset_results.csv`.

These results describe simulator experiments, not hardware performance.

## Processor Architectures

Processor definitions are stored in the `processors/` directory.

### Processor A

* Physical qubits: 5
* Coupling edges: `(0,1), (1,2), (2,3), (3,4)`
* Direct one-to-one mapping of all six logical qubits is infeasible because only five physical qubits are available.

### Processor B

* Physical qubits: 9
* Coupling edges: `(0,1), (1,2), (2,3), (2,4), (4,5), (5,6), (4,7), (7,8)`
* A direct mapping is feasible by qubit count. This does not, by itself, prove that every circuit interaction can be implemented without routing overhead.

### Processor D

* Physical qubits: 6
* Coupling edges: `(0,1), (0,2), (0,5), (1,2), (1,3), (2,3), (2,4), (3,4), (3,5), (4,5)`
* Proposed workload-aware architecture designed for the six-qubit `graph_01` practice instance.
* This is a synthetic topology for routing studies, not a real quantum processor.
* Its potential advantage must be evaluated against the chosen graph and benchmark settings; it should not be assumed to generalize to other workloads.

The Processor D definition is stored in `processors/processor_D.json`.

## Ideal Transpilation Results

The existing routing benchmark evaluates `graph_01` for the current Processor A, B, and D configurations.

| Processor   | Physical qubits | Circuit depth | Total gates | CX count | Explicit SWAP count |
| ----------- | --------------: | ------------: | ----------: | -------: | ------------------: |
| Processor A |               5 |    Infeasible |           — |        — |                   — |
| Processor B |               9 |           123 |         218 |       41 |                   0 |
| Processor D |               6 |            35 |          78 |       20 |                   0 |

These metrics come from the ideal transpilation experiment. They are not quantum hardware measurements.

For this particular run, Processor D had approximately 71.5% lower circuit depth and 51.2% fewer CX gates than Processor B. These are results for one team-created graph, one parameter setting, and one transpilation configuration—not a universal performance guarantee.

An explicit SWAP count of zero does not establish zero routing overhead. Routing, layout selection, and gate decomposition can affect depth and gate counts without leaving explicit SWAP instructions in the final circuit.

The graph-specific routing results are stored in `results/tables/processor_routing_graph01_comparison.csv`.

## Noisy QAOA Simulation

Noisy simulation uses Qiskit Aer with the following error settings:

| Error type                       | Configured probability |
| -------------------------------- | ---------------------: |
| Single-qubit depolarizing error  |                  0.001 |
| CX depolarizing error            |                  0.005 |
| Symmetric readout bit-flip error |                   0.01 |

The benchmark uses 4,096 shots and fixed QAOA parameters `gamma = 0.1` and `beta = 0.3`.

### Preliminary noisy result for graph_01

| Metric                  |  Result |
| ----------------------- | ------: |
| Circuit depth           |      36 |
| Total gates             |      84 |
| CX count                |      20 |
| Average cut weight      | 18.9456 |
| Best sampled cut        |      26 |
| Classical optimum       |      26 |
| Optimal-cut probability |  11.79% |

This preliminary run is a generic gate-noise simulation and is not a processor-specific hardware result.

The script is `src/noisy_qaoa_graph01.py`. Its output is `results/tables/noisy_qaoa_graph01.csv`.

### Noisy Processor B vs. Processor D comparison

The topology-aware comparison uses the same practice graph, QAOA parameters, gate-noise rates, shot count, and transpilation settings for both processor configurations.

| Metric                  | Processor B | Processor D |
| ----------------------- | ----------: | ----------: |
| Physical qubits         |           9 |           6 |
| Circuit depth           |         124 |          36 |
| Total gates             |         224 |          84 |
| CX count                |          41 |          20 |
| Explicit SWAP count     |           0 |           0 |
| Average cut weight      |     18.5852 |     18.9456 |
| Best sampled cut        |          26 |          26 |
| Optimal-cut probability |      10.57% |      11.79% |

In this run, Processor D had approximately 71.0% lower circuit depth and 51.2% fewer CX gates than Processor B. Its average cut weight was approximately 0.36 higher, and its optimal-cut probability was approximately 1.22 percentage points higher.

These findings are consistent with a potential advantage from the proposed topology for this particular workload. They do not prove that connectivity alone caused the difference or that Processor D would outperform Processor B on other graphs or actual hardware.

The comparison script is `src/noisy_processor_comparison.py`. Its output is `results/tables/noisy_processor_comparison_graph01.csv`.

**Noise-model limitation:** The configured error rates are simulation assumptions. The results are not calibrated predictions of a physical device. Further validation should check the exact noise-model requirements in the official challenge materials, repeat experiments with appropriate seeds, and evaluate additional official benchmark instances.

## Project Structure

```text
maxcut-practice/
├── data/
│   └── raw/
│       └── maxcut_instances.json
├── processors/
│   ├── processor_A.json
│   ├── processor_B.json
│   └── processor_D.json
├── results/
│   ├── figures/
│   └── tables/
│       ├── classical_optima.csv
│       ├── qaoa_optimization.csv
│       ├── qaoa_dataset_results.csv
│       ├── processor_routing_graph01_comparison.csv
│       ├── noisy_qaoa_graph01.csv
│       └── noisy_processor_comparison_graph01.csv
├── src/
│   ├── maxcut_classical.py
│   ├── maxcut_qaoa.py
│   ├── optimize_dataset_qaoa.py
│   ├── qaoa_dataset_benchmark.py
│   ├── processor_routing_benchmark.py
│   ├── noisy_qaoa_graph01.py
│   ├── noisy_processor_comparison.py
│   ├── consolidate_results.py
│   └── plot_benchmark_results.py
├── requirements.txt
├── requirements-lock.txt
└── README.md
```

Other practice scripts and result files may also be present in the repository.

## Requirements

The environment used for the latest experiments includes:

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

## Running Experiments

Run commands from the repository root. If the virtual environment is active, use `python`; otherwise, use the interpreter inside `.venv`.

```powershell
python .\src\maxcut_classical.py
python .\src\qaoa_dataset_benchmark.py
python .\src\optimize_dataset_qaoa.py
python .\src\processor_routing_benchmark.py
python .\src\noisy_qaoa_graph01.py
python .\src\noisy_processor_comparison.py
python .\src\consolidate_results.py
python .\src\plot_benchmark_results.py
```

Review regenerated outputs before committing them. Some scripts overwrite their output CSV files. Older scripts may run separate illustrative experiments and should not be mixed with the six-vertex benchmark unless their differences are documented.

## Limitations and Future Work

* The three graphs are team-created practice inputs, not official fixed benchmark instances.
* The parameter search is a coarse grid and does not guarantee globally optimal parameters.
* Processor A cannot directly map all six logical qubits onto five physical qubits using a one-to-one mapping.
* Processor D is a proposed synthetic topology, not a physical processor.
* Transpilation and Aer simulation metrics are not hardware results.
* A zero explicit SWAP count does not establish zero routing overhead.
* The noise model uses configured error rates rather than calibration data from a real device.
* The current processor comparison focuses on `graph_01`; broader evaluation is required before drawing general conclusions.
* Official benchmark instances, organizer settings, and final architecture requirements must be checked against the released challenge materials before claiming full compliance.
* A final technical report, reproducibility checks, and any required submission artifacts should be completed before submission.

## Team Information

**Team:** NexGen Minds
**Challenge:** Qiskit Fall Fest SRMAP 2026 — PS-O1: Max-Cut on Weighted Graphs
