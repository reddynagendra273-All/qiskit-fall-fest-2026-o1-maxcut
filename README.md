# NexGen Minds | QAOA Max-Cut Optimization

**Qiskit Fall Fest SRMAP 2026 — PS-O1: Max-Cut on Weighted Graphs**

This project explores the Quantum Approximate Optimization Algorithm (QAOA) for solving weighted Max-Cut problems and investigates how processor connectivity affects quantum circuit transpilation.

**Project Status:** Practice simulations and ideal transpilation experiments. No actual quantum hardware measurements are claimed.

## Project Objectives

* Compute exact classical Max-Cut solutions using brute force.
* Construct and simulate p=1 QAOA circuits.
* Explore parameter selection using a coarse parameter grid.
* Compare circuit metrics for the specified Processor A and Processor B architectures.
* Analyze circuit depth, total gate count, CX count, and explicit SWAP count.

## Dataset and Classical Results

The practice dataset contains three weighted graphs, each with six vertices and integer edge weights. These are team-created examples and are not official fixed benchmark instances.

| Graph    | Classical Optimum | Optimal Assignments | Assignments Checked |
| -------- | ----------------: | ------------------: | ------------------: |
| graph_01 |                26 |                   2 |                  64 |
| graph_02 |                27 |                   2 |                  64 |
| graph_03 |                24 |                   4 |                  64 |

The graph definitions are stored in `data/raw/maxcut_instances.json`.

The exact classical results are stored in `results/tables/classical_optima.csv`.

The classical optimum is the maximum total weight of edges crossing between the two vertex groups.

## QAOA Parameter Search

The parameter-grid search evaluates 32 combinations per graph, using 2,048 shots and simulator seed 42. The reported parameters are the best candidates within the tested grid, selected by average cut weight. They are not guaranteed to be globally optimal.

| Graph    | Classical Optimum | Average Cut Weight | Average Approximation Ratio | Optimal-Cut Probability |
| -------- | ----------------: | -----------------: | --------------------------: | ----------------------: |
| graph_01 |                26 |            19.3081 |                      0.7426 |                0.135742 |
| graph_02 |                27 |            19.1533 |                      0.7094 |                0.125977 |
| graph_03 |                24 |            19.2256 |                      0.8011 |                0.183105 |

The complete parameter-search results are available in `results/tables/qaoa_optimization.csv`.

The fixed-parameter simulation results are available in `results/tables/qaoa_dataset_results.csv`.

The average approximation ratio is calculated by dividing the average sampled cut weight by the exact classical optimum.

## Processor A and Processor B Architecture Analysis

The processor definitions are stored in `processors/processor_A.json` and `processors/processor_B.json`.

| Processor   | Physical Qubits | Coupling Edges                                                                     |
| ----------- | --------------: | ---------------------------------------------------------------------------------- |
| Processor A |               5 | (0,1), (1,2), (1,3), (3,4)                                                         |
| Processor B |               9 | (0,1), (1,2), (1,6), (2,3), (2,6), (2,5), (3,4), (4,5), (5,6), (6,7), (6,8), (8,0) |

Each graph requires six logical qubits. Processor A has only five physical qubits, so a direct one-to-one mapping of all six logical qubits is infeasible. Processor B has enough physical qubits for such a mapping.

### Processor B Transpilation Results

| Graph    | Circuit Depth | Total Gates | CX Count | Explicit SWAP Count |
| -------- | ------------: | ----------: | -------: | ------------------: |
| graph_01 |            79 |         157 |       35 |                   0 |
| graph_02 |            89 |         169 |       38 |                   0 |
| graph_03 |           104 |         191 |       42 |                   0 |

These values are results from the current ideal transpilation setup, not quantum hardware measurements.

A zero explicit SWAP count does not prove that routing added no overhead. Routing effects can be reflected in the decomposed gate sequence and other circuit metrics. CX count is not an exact SWAP count.

The detailed processor comparison is stored in `results/tables/processor_routing_comparison.csv`.

The consolidated benchmark results are stored in `results/tables/consolidated_benchmark.csv`.

**Noise Model Note:** Processor noise parameters have not been verified in this repository. Any noise-aware comparison must use the definitions supplied in the official Challenge Kit.

## Figures and Visualizations

The repository includes the following figures:

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
└── README.md
```

Additional practice scripts and result files are included in the repository.

## Requirements

The current working environment uses Python 3.14.7, Qiskit 2.5.2, and Qiskit Aer 0.17.2. Other software versions may produce different results.

The project dependencies are listed in `requirements.txt`:

* Qiskit
* Qiskit Aer
* NumPy
* Matplotlib
* NetworkX

## Installation

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/reddynagendra273-All/qiskit-fall-fest-2026-o1-maxcut.git
cd qiskit-fall-fest-2026-o1-maxcut
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```powershell
python -m pip install -r requirements.txt
```

If a virtual environment already exists, use its Python executable directly instead of creating another one.

## Running the Dataset Benchmark

Run the following commands from the repository root in PowerShell:

```powershell
.\.venv\Scripts\python.exe src\maxcut_classical.py
.\.venv\Scripts\python.exe src\qaoa_dataset_benchmark.py
.\.venv\Scripts\python.exe src\optimize_dataset_qaoa.py
.\.venv\Scripts\python.exe src\processor_routing_benchmark.py
.\.venv\Scripts\python.exe src\consolidate_results.py
.\.venv\Scripts\python.exe src\plot_benchmark_results.py
```

These scripts regenerate the classical results, QAOA simulation results, processor-routing metrics, consolidated table, and figures. Review the output files before committing any regenerated results.

Older scripts in the `src` directory may perform separate illustrative routing experiments. Their results should not be mixed with the six-vertex Processor A and Processor B benchmark unless the differences in experimental setup are clearly explained.

## Reproducibility and Limitations

* The three graph instances are team-created practice inputs, not official fixed benchmark instances.
* QAOA results depend on parameter values, shot count, simulator seed, circuit construction, and software versions.
* The parameter search is a coarse grid and does not guarantee globally optimal parameters.
* Processor metrics are transpilation outputs; no actual quantum hardware execution is claimed.
* Processor A cannot directly accommodate six logical qubits through a one-to-one mapping because it has only five physical qubits.
* Processor noise parameters must be verified against the official Challenge Kit before making noise-related claims.
* A clean-environment reproduction test and final submission review remain necessary.
* The repository still needs a submission entry point (`main.py` or `main.ipynb`) and a final report or analysis artifact if required by the organizer checklist.

## Team Information

**Team Name:** NexGen Minds

**Challenge:** Qiskit Fall Fest SRMAP 2026 — PS-O1: Max-Cut on Weighted Graphs
