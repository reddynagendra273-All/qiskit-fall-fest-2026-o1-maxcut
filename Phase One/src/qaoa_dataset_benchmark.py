import csv
import json
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "raw" / "maxcut_instances.json"
OPTIMA_PATH = ROOT / "results" / "tables" / "classical_optima.csv"
OUTPUT_PATH = ROOT / "results" / "tables" / "qaoa_dataset_results.csv"

GAMMA = 0.5
BETA = 0.3
SHOTS = 4096
SEED = 42

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
    # Qiskit displays classical bits in reverse qubit order.
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

    qc = QuantumCircuit(n, n)

    # Initial equal superposition.
    for q in range(n):
        qc.h(q)

    # Weighted Max-Cut cost layer, p = 1.
    for u, v, weight in edges:
        qc.rzz(-GAMMA * weight, u, v)

    # Mixer layer.
    for q in range(n):
        qc.rx(2 * BETA, q)

    qc.measure(range(n), range(n))

    compiled = transpile(
        qc, simulator, optimization_level=0
    )
    counts = simulator.run(
        compiled, shots=SHOTS, seed_simulator=SEED
    ).result().get_counts()

    sampled_weights = {
        bits: cut_weight(bits, edges)
        for bits in counts
    }

    best_weight = max(sampled_weights.values())
    average_weight = sum(
        sampled_weights[bits] * count
        for bits, count in counts.items()
    ) / SHOTS

    optimal_shots = sum(
        count for bits, count in counts.items()
        if sampled_weights[bits] == optimum
    )

    approximation_ratio = best_weight / optimum
    optimal_probability = optimal_shots / SHOTS

    ops = compiled.count_ops()

    row = {
        "graph_id": graph_id,
        "vertices": n,
        "edges": len(edges),
        "qaoa_layers": 1,
        "gamma": GAMMA,
        "beta": BETA,
        "shots": SHOTS,
        "classical_optimum": optimum,
        "best_sampled_cut": best_weight,
        "average_cut": round(average_weight, 4),
        "best_sampled_approximation_ratio": round(
            approximation_ratio, 4
        ),
        "optimal_cut_probability": round(optimal_probability, 6),
        "circuit_depth": compiled.depth(),
        "total_gates": compiled.size(),
        "cx_count": ops.get("cx", 0),
        "swap_count": ops.get("swap", 0),
    }
    results.append(row)

    print(f"\n{graph_id}")
    print("-" * 40)
    for key, value in row.items():
        print(f"{key}: {value}")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print(f"\nSaved results to: {OUTPUT_PATH.relative_to(ROOT)}")
print("SIMULATOR PRACTICE RESULTS — not hardware measurements.")
print("Parameters are fixed, not optimized.")
