
# PRACTICE ONLY â€” NOT OFFICIAL HACKATHON DATA
# QAOA routing overhead analysis with CSV export

import csv
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap

N = 5
GAMMA = 0.26
BETA = 0.42
SEED = 42

EDGES = [
    (0, 1, 3),
    (0, 2, 2),
    (1, 2, 1),
    (1, 3, 4),
    (2, 4, 2),
    (3, 4, 3),
]

BASIS = ["rz", "sx", "x", "cx"]

def build_qaoa():
    qc = QuantumCircuit(N)

    for q in range(N):
        qc.h(q)

    for u, v, weight in EDGES:
        qc.rzz(-GAMMA * weight, u, v)

    for q in range(N):
        qc.rx(2 * BETA, q)

    return qc

base = build_qaoa()

linear = CouplingMap(couplinglist=[
    (0, 1), (1, 2), (2, 3), (3, 4)
])

ring = CouplingMap(couplinglist=[
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 0)
])

configs = [
    ("Unrestricted", None),
    ("Practice Linear", linear),
    ("Practice Ring", ring),
]

rows = []

for name, coupling in configs:
    options = {
        "basis_gates": BASIS,
        "optimization_level": 0,
        "seed_transpiler": SEED,
    }

    if coupling is not None:
        options.update({
            "coupling_map": coupling,
            "initial_layout": list(range(N)),
            "routing_method": "sabre",
        })

    circuit = transpile(base, **options)
    ops = circuit.count_ops()

    rows.append({
        "configuration": name,
        "depth": circuit.depth(),
        "total_gates": circuit.size(),
        "cx_gates": ops.get("cx", 0),
        "explicit_swap_gates": ops.get("swap", 0),
    })

baseline = rows[0]

print("\nROUTING OVERHEAD ANALYSIS")
print("=" * 76)
print(
    f"{'Configuration':<20} {'Depth':>8} "
    f"{'Gates':>8} {'CX':>8} {'Depth overhead':>17}"
)

for row in rows:
    depth_overhead = (
        100 * (row["depth"] - baseline["depth"])
        / baseline["depth"]
    )

    cx_overhead = (
        100 * (row["cx_gates"] - baseline["cx_gates"])
        / baseline["cx_gates"]
    )

    row["depth_overhead_percent"] = round(depth_overhead, 2)
    row["cx_overhead_percent"] = round(cx_overhead, 2)

    print(
        f"{row['configuration']:<20} "
        f"{row['depth']:>8} "
        f"{row['total_gates']:>8} "
        f"{row['cx_gates']:>8} "
        f"{depth_overhead:>15.2f}%"
    )

filename = "results/tables/routing_analysis_results.csv"

with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"\nResults saved to {filename}")
print("Practice simulation only; no hardware execution.")
print("CX overhead is a proxy, not an exact SWAP count.")

