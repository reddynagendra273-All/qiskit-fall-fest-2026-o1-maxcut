# Qiskit Fall Fest 2026 — Phase 1 PS-O1 Report

## 1. Problem statement

This project studies the weighted Max-Cut problem using QAOA and compares quantum processor architectures A and B through circuit mapping and routing analysis.

## 2. Official graph

The official instance contains 6 vertices and 9 weighted edges. The graph was generated using NetworkX Erdos-Renyi generation with n=6, p=0.5, and graph seed 42. Edge weights are integers from 1 to 5; the weight-generation seed is documented separately in the instance JSON for reproducibility.

## 3. Classical reference

All 2^6 = 64 possible bit assignments were checked. The exact classical maximum cut value is 16. Two optimal bitstrings were found: 001011 and 110100.

## 4. QAOA benchmark

The official graph was evaluated using a generic Qiskit Aer simulator with 4,096 shots per parameter configuration. The tested grid contained 8 gamma values and 4 beta values.

| Metric | Result |
|---|---:|
| Best gamma | 0.3 |
| Best beta | 0.3 |
| Exact classical optimum | 16 |
| Best sampled cut | 16 |
| Average cut | 11.6611 |
| Average approximation ratio | 0.7288 |
| Best sampled approximation ratio | 1.0 |
| Optimal-cut probability | 0.14209 |

The best sampled cut reaches the exact classical optimum. This does not mean every measurement returns an optimal solution: the observed optimal-cut probability was approximately 14.209%.

Results are saved in `results/tables/official_qaoa_optimization.csv`.

## 5. Processor architecture analysis

Processor A and Processor B are represented by the topology files in `processors/`. The routing comparison is recorded in `results/tables/processor_routing_comparison.csv`.

The architecture comparison must be interpreted using the documented logical-to-physical mappings and transpiled circuit metrics. The generic official-instance QAOA benchmark above is not a Processor A/B hardware execution and must not be presented as one.

## 6. Reproducibility

Use the project's Python environment and dependencies from `requirements.txt`. The official graph JSON records its graph-generation parameters and weight-generation choice. The benchmark script records its parameter grid, shot count, and simulation seed.

## 7. Limitations

The reported official-instance benchmark is a generic simulator result. Processor-specific performance claims should be based only on the corresponding transpiled routing data or explicitly documented noise simulations.
