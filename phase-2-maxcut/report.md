# QFF 2026 Phase 2 — PS-O1 Weighted Max-Cut Report

## 1. Problem and objective

PS-O1 asks us to solve a weighted Max-Cut instance with six logical vertices. Each vertex is assigned to one of two partitions, and an edge contributes its weight when its endpoints are placed in different partitions. The objective is to maximize the total weight of cut edges.

The locked instance used in this work has nine weighted edges with total weight 27. Exhaustive enumeration of all 64 bitstrings gives an exact classical optimum of 22. The two optimal bitstrings under the stated `x0...x5` convention are `001011` and `110100`; they represent complementary partitions.

## 2. Method

The solver uses a depth-one (p=1) Quantum Approximate Optimization Algorithm (QAOA) circuit. Parameters are optimized against an ideal statevector objective using COBYLA and five initial seeds (0–4), with gamma and beta sampled from [0, π]. The selected angles are then evaluated on the available processor topologies using the official helper module and configured ideal/noisy simulation settings.

Processor A has five qubits and cannot execute the six-qubit logical circuit. It is therefore reported as not executable rather than assigned fabricated performance numbers. Processor B has nine qubits. Processor D is the team-designed six-qubit topology.

## 3. Benchmark results

The run recorded the following values:

| Processor | Condition | Mean sampled cut | Approximation ratio (mean / 22) | Best sampled cut | P(optimal set) | CX | Depth | SWAPs |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| B | Ideal | 17.76196 | 0.80736 | 22 | 0.13965 | 21 | 37 | 1 |
| B | Noisy | 17.32202 | 0.78736 | 22 | 0.12598 | 21 | 37 | 1 |
| D | Ideal | 17.71338 | 0.80515 | 22 | 0.13843 | 18 | 29 | 0 |
| D | Noisy | 17.29614 | 0.78619 | 22 | 0.12500 | 18 | 29 | 0 |

All values above are simulator results, not measurements on physical quantum hardware. The ideal/noisy comparison suggests that the configured noise reduces the mean cut and probability of sampling an optimum for both executable processors.

Processor D uses three fewer transpiled CX gates than Processor B for this circuit (18 versus 21), has no inserted SWAPs (versus one), and has lower circuit depth (29 versus 37). However, Processor B's noisy mean cut is slightly higher in this particular run (17.32202 versus 17.29614). The small quality difference should not be overinterpreted; it is a single seeded simulation configuration.

## 4. Classical and random baselines

The exact optimum is 22. The total edge weight is 27. For a uniformly random bipartition, each edge is cut with probability 1/2, so the expected random cut weight is 13.5. Its expected approximation ratio relative to the exact optimum is 13.5 / 22 ≈ 0.61364.

**CSV schema caution:** the current `results.csv` has `random_baseline=0.5`. This value may mean the per-edge cut probability, but it is not the expected cut weight (13.5) or the expected approximation ratio (0.61364). Check the challenge kit's intended units for that column and fix the generator before final submission. Do not leave an ambiguous mixture of probability, cut weight, and ratio.

## 5. Bell-state experiment on Processor D

The Bell test checks an adjacent pair (0, 2) and a farthest pair (0, 1), under ideal and noisy simulation. The measured correlations and fidelities are stored in `results/tables/bell.csv`.

| Pair | Condition | XX | YY | ZZ | Fidelity ± SE |
|---|---|---:|---:|---:|---:|
| Adjacent (0,2) | Ideal | 1.0000 | -1.0000 | 1.0000 | 1.0000 ± 0.0000 |
| Adjacent (0,2) | Noisy | 0.9458 | -0.9521 | 0.9551 | 0.9633 ± 0.0021 |
| Farthest (0,1) | Ideal | 1.0000 | -1.0000 | 1.0000 | 1.0000 ± 0.0000 |
| Farthest (0,1) | Noisy | 0.9443 | -0.9341 | 0.9385 | 0.9542 ± 0.0023 |

The target state is |Φ+⟩, for which the expected correlations are XX = +1, YY = −1, and ZZ = +1. The noisy fidelity is lower for the farthest pair in this simulation. The farthest pair requires more routing CX gates than the adjacent pair, so extra circuit operations are a plausible contributor; this is an interpretation of the simulated topology, not a hardware finding.

## 6. Limitations and risks

- Results are simulator-based and depend on the selected QAOA parameters, transpilation, random seeds, shot count, and noise model.
- p=1 QAOA is a limited-depth heuristic and is not guaranteed to reach the exact optimum consistently.
- The exact optimum is sampled at least once in the reported runs, but best-sampled cut alone does not describe typical solution quality; mean cut and P(optimal set) are also reported.
- Python 3.14.7 was used in the current local environment, but the starter README specifies Python 3.10–3.12. Re-run in a supported Python 3.12 environment before claiming full official-environment reproducibility.
- Verify the exact `random_baseline` CSV definition against the challenge kit.
- Confirm the final Processor D JSON is frozen, validated, and identical to the version represented in the report and figures.

## 7. Reproduction steps

1. Use Python 3.12 and install the pinned, tested dependencies.
2. Confirm `processors/processor_D.json` and the locked instance against the official kit.
3. Run `python solve_ps_o1_phase2.py` from the project root.
4. Open `main.ipynb` in Jupyter and run every cell top-to-bottom.
5. Check that the CSV files and PNG figures were generated and that the values in this report match the regenerated outputs.
6. Include the required AI-assistance disclosure in the repository if the event rules require it.

## 8. AI-assistance disclosure

AI assistance was used to help structure documentation and analysis and to prepare reproducibility materials. The team should review, understand, validate, and take responsibility for every submitted result and code change.
