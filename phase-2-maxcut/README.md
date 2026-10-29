##### \# QFF 2026 Phase 2 - PS-O1 Weighted Max-Cut


##### This folder contains our Phase 2 implementation and benchmark results for PS-O1, a weighted Max-Cut optimization problem. The project uses the Quantum Approximate Optimization Algorithm (QAOA), classical parameter optimization, processor-topology analysis, and ideal/noisy simulator experiments.


##### \## 1. Problem Summary


##### The problem instance contains six logical vertices and nine weighted edges, with a total edge weight of 27.


##### Exhaustive evaluation of all 64 possible bitstrings gives an exact classical optimum cut weight of \*\*22\*\*. Under the project's stated bitstring convention, the optimal bitstrings are `001011` and `110100`, representing complementary partitions.


##### \## 2. Benchmark Results


##### The following results were recorded for the executable processor configurations.


##### | Processor | Condition | Mean Cut | Approximation Ratio | CX Gates | Circuit Depth | SWAPs |

##### |---|---|---:|---:|---:|---:|---:|

##### | B | Ideal | 17.76196 | 0.80736 | 21 | 37 | 1 |

##### | B | Noisy | 17.32202 | 0.78736 | 21 | 37 | 1 |

##### | D | Ideal | 17.71338 | 0.80515 | 18 | 29 | 0 |

##### | D | Noisy | 17.29614 | 0.78619 | 18 | 29 | 0 |


##### The approximation ratio is calculated as the mean cut divided by the exact classical optimum of 22.


##### Processor A is not executable for this instance because it provides five physical qubits, while the problem requires six logical qubits.


##### All values are results from simulation, not measurements from physical quantum hardware. In this run, Processor D uses three fewer transpiled CX gates than Processor B, requires no inserted SWAP gates, and has a lower circuit depth. Processor B has a slightly higher noisy mean cut in this particular simulation, so circuit efficiency and solution quality should be considered separately.


##### \## 3. Classical and Random Baselines


##### The exact classical optimum is 22.


##### For a uniformly random bipartition, each edge has a probability of 0.
