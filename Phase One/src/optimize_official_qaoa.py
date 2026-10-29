import csv
import json
import random
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "raw" / "official_maxcut_instance.json"
OUTPUT_PATH = ROOT / "results" / "tables" / "official_qaoa_optimization.csv"

SHOTS = 4096
SEED = 42
GAMMAS = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5]
BETAS = [0.1, 0.3, 0.5, 0.7]

data = json.loads(DATA_PATH.read_text(encoding="utf-8-sig"))
graph = data["graphs"][0]
edges = graph["edges"]
n = data["num_vertices"]

if OUTPUT_PATH.exists():
    raise FileExistsError(f"Refusing to overwrite existing results: {OUTPUT_PATH}")

optimum = max(
    sum(w for u, v, w in edges
        if ((mask >> u) & 1) != ((mask >> v) & 1))
    for mask in range(1 << n)
)

def cut_weight(bitstring):
    bits = bitstring.replace(" ", "")[::-1]
    return sum(w for u, v, w in edges if bits[u] != bits[v])

simulator = AerSimulator()
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

        compiled = transpile(qc, simulator, optimization_level=0, seed_transpiler=SEED)
        counts = simulator.run(compiled, shots=SHOTS, seed_simulator=SEED).result().get_counts()
        weights = {bits: cut_weight(bits) for bits in counts}
        average = sum(weights[bits] * count for bits, count in counts.items()) / SHOTS
        best_cut = max(weights.values())
        candidate = {
            "graph_id": graph["id"],
            "gamma": gamma,
            "beta": beta,
            "shots": SHOTS,
            "classical_optimum": optimum,
            "best_sampled_cut": best_cut,
            "average_cut": round(average, 4),
            "average_approximation_ratio": round(average / optimum, 4),
            "best_sampled_approximation_ratio": round(best_cut / optimum, 4),
            "optimal_cut_probability": round(
                sum(count for bits, count in counts.items() if weights[bits] == optimum) / SHOTS, 6
            ),
        }
        if best is None or candidate["average_cut"] > best["average_cut"]:
            best = candidate

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=best.keys())
    writer.writeheader()
    writer.writerow(best)

print("Official graph:", graph["id"])
print("Exact classical optimum:", optimum)
for key, value in best.items():
    print(f"{key}: {value}")
print("Saved to:", OUTPUT_PATH.relative_to(ROOT))
print("Generic simulator only; not Processor A/B or hardware results.")
