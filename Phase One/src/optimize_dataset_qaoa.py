import csv
import json
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "raw" / "maxcut_instances.json"
OPTIMA_PATH = ROOT / "results" / "tables" / "classical_optima.csv"
OUTPUT_PATH = ROOT / "results" / "tables" / "qaoa_optimization.csv"

SHOTS = 4096
SEED = 42

# Coarse grid first; refine later around the best candidates.
GAMMAS = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5]
BETAS = [0.1, 0.3, 0.5, 0.7]

with DATA_PATH.open("r", encoding="utf-8-sig") as f:
    dataset = json.load(f)

with OPTIMA_PATH.open("r", newline="", encoding="utf-8-sig") as f:
    optima = {
        row["graph_id"]: int(row["classical_optimum"])
        for row in csv.DictReader(f)
    }

simulator = AerSimulator(seed_simulator=SEED)
results = []


def cut_weight(bitstring, edges):
    bits = bitstring.replace(" ", "")[::-1]
    return sum(
        weight for u, v, weight in edges
        if bits[u] != bits[v]
    )


for graph in dataset["graphs"]:
    graph_id = graph["id"]
    edges = graph["edges"]
    n = dataset["num_vertices"]
    optimum = optima[graph_id]

    best = None

    for gamma in GAMMAS:
        for beta in BETAS:
            qc = QuantumCircuit(n, n)

            for q in range(n):
                qc.h(q)

            for u, v, weight in edges:
                qc.rzz(-gamma * weight, u, v)

            for q in range(n):
                qc.rx(2 * beta, q)

            qc.measure(range(n), range(n))

            compiled = transpile(
                qc, simulator, optimization_level=0
            )
            counts = simulator.run(
                compiled,
                shots=SHOTS,
                seed_simulator=SEED,
            ).result().get_counts()

            weights = {
                bits: cut_weight(bits, edges)
                for bits in counts
            }

            average = sum(
                weights[bits] * count
                for bits, count in counts.items()
            ) / SHOTS

            best_cut = max(weights.values())

            candidate = {
                "graph_id": graph_id,
                "gamma": gamma,
                "beta": beta,
                "shots": SHOTS,
                "classical_optimum": optimum,
                "best_sampled_cut": best_cut,
                "average_cut": round(average, 4),
                "average_approximation_ratio": round(
                    average / optimum, 4
                ),
                "best_sampled_approximation_ratio": round(
                    best_cut / optimum, 4
                ),
                "optimal_cut_probability": round(
                    sum(
                        count for bits, count in counts.items()
                        if weights[bits] == optimum
                    ) / SHOTS,
                    6,
                ),
            }

            # Select parameters by expected (average) cut weight.
            if best is None or candidate["average_cut"] > best["average_cut"]:
                best = candidate

    results.append(best)
    print(f"\nBest grid candidate for {graph_id}:")
    for key, value in best.items():
        print(f"{key}: {value}")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print(f"\nSaved to: {OUTPUT_PATH.relative_to(ROOT)}")
print("Coarse grid search; not guaranteed to find global optimum.")
print("Simulator results only, not hardware measurements.")
