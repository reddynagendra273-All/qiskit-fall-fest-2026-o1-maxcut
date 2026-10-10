# O1 Max-Cut: Quantum Optimization with Qiskit

**Qiskit Fall Fest 2026 — Phase 1 Hackathon**

## 1. Project Overview

This project explores the Max-Cut optimization problem using quantum computing concepts and Qiskit. The main objective is to divide the vertices of a graph into two groups so that the number of edges connecting vertices in different groups is maximized.

The project will investigate how a quantum optimization approach can be used to solve this problem and how its performance can be evaluated across two specified processor configurations.

Rather than focusing only on obtaining a solution, this project aims to study solution quality, circuit complexity, and execution performance using measurable results.

## 2. Problem Statement

Given an undirected graph \(G=(V,E)\), the task is to assign every vertex to one of two sets. An edge contributes to the cut when its endpoints belong to different sets.

The objective is to find a partition that maximizes the total number of cut edges.

Mathematically, the objective is:

$$
\max \sum_{(u,v)\in E} [x_u \ne x_v]
$$

where \(x_u\) and \(x_v\) represent the group assignments of the two endpoints, and the indicator contributes 1 when their assignments differ and 0 otherwise.

## 3. Project Objectives

* Understand and formulate the Max-Cut problem as a graph optimization task.
* Develop a reproducible solution using Python and Qiskit.
* Implement the algorithm specified by the official O1 challenge requirements.
* Evaluate the solution using the designated Processor A and Processor B configurations.
* Record and analyze objective values and relevant circuit and execution metrics.
* Compare results using evidence rather than assumptions.
* Document the implementation, experimental setup, limitations, and findings.

## 4. Proposed Methodology

The project will follow a structured workflow:

1. **Requirement analysis:** Identify the official graph instance, algorithm, processor configurations, evaluation metrics, and submission requirements.
2. **Problem formulation:** Represent the supplied graph and define the Max-Cut objective.
3. **Implementation:** Develop the required solution using Python and the appropriate Qiskit components.
4. **Validation:** Check the objective calculation and verify that the implementation produces valid results.
5. **Processor evaluation:** Run the same solution under the prescribed Processor A and Processor B configurations.
6. **Results analysis:** Compare the measured outcomes, circuit characteristics, and execution costs where applicable.
7. **Reproducibility:** Organize the source code, environment requirements, experimental outputs, and documentation.

The final implementation will follow the official challenge kit rather than assume an algorithm or hardware configuration before those requirements are confirmed.

## 5. Evaluation Criteria

The evaluation will use the metrics required by the official challenge specification. Depending on the prescribed evaluation, these may include:

* Cut value or objective quality
* Circuit depth
* Two-qubit gate count
* Qubit usage
* Routing and SWAP overhead
* Runtime or execution cost

The final report will distinguish measured results from theoretical expectations and will explain any limitations affecting the comparison.

## 6. Planned Repository Structure

```text
O1-MaxCut-Project/
├── README.md
├── main.ipynb
├── requirements.txt
├── data/
├── processors/
├── src/
└── results/
    ├── tables/
    └── figures/
```

The final structure will be aligned with the official Phase 1 submission template and any required starter files.

## 7. Reproducibility and Documentation

Reproducibility is an important part of this project. The repository will document the software environment, input data, processor configurations, execution procedure, and generated results. Where possible, experiments will use consistent settings so that the comparison is meaningful.

## 8. Current Status

**Stage 1 — Repository setup completed.**

The GitHub repository has been created. The next stage is to verify the official O1 challenge requirements and prepare the project environment before implementing the solution.

Processor comparisons, experimental findings, and conclusions will be added after the required experiments have been completed.

## 9. Expected Outcome

The expected outcome is a documented and reproducible Max-Cut implementation that follows the Phase 1 requirements, evaluates the prescribed processor configurations, and presents a clear, evidence-based analysis of the results.

This project is being developed iteratively, with emphasis on correctness, transparent experimentation, and understanding the relationship between quantum optimization and practical execution constraints.
