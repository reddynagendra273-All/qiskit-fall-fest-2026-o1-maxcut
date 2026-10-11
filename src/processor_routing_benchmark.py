import csv
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap
from qiskit_aer import AerSimulator

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "tables" / "processor_routing_comparison.csv"

# Five-vertex practice graph; not an official fixed challenge instance.
edges = [
    (0, 1, 3),
    (0, 2, 2),
    (1, 2, 1),
    (1, 3, 4),
    (2, 4, 2),
    (3, 4, 3),
]

gamma = 0.1
beta = 0.3

processors = {
    "Processor A": {
        "num_qubits": 5,
        "coupling": [(0, 1), (1, 2), (1, 3), (3, 4)],
    },
    "Processor B": {
        "num_qubits": 9,
        "coupling": [
            (0, 1), (1, 2), (1, 6), (2, 3),
            (2, 6), (2, 5), (3, 4), (4, 5),
            (5, 6), (6, 7), (6, 8), (8, 0),
        ],
    },
}

qc = QuantumCircuit(5)
for q in range(5):
    qc.h(q)

for u, v, weight in edges:
    qc.rzz(-gamma * weight, u, v)

for q in range(5):
    qc.rx(2 * beta, q)

basis_gates = ["rz", "sx", "x", "cx"]

simulator = AerSimulator()
rows = []

for name, config in processors.items():
    coupling = CouplingMap(config["coupling"])

    compiled = transpile(
        qc,
        basis_gates=basis_gates,
        coupling_map=coupling,
        initial_layout=list(range(5)),
        optimization_level=3,
        seed_transpiler=42,
    )

    ops = compiled.count_ops()

    row = {
        "processor": name,
        "physical_qubits_available": config["num_qubits"],
        "logical_qubits_used": 5,
        "coupling_edges": len(config["coupling"]),
        "depth": compiled.depth(),
        "total_gates": compiled.size(),
        "cx_count": ops.get("cx", 0),
        "explicit_swap_count": ops.get("swap", 0),
        "basis_gates": ",".join(basis_gates),
        "gamma": gamma,
        "beta": beta,
        "status": "ideal transpilation; not hardware execution",
    }
    rows.append(row)

    print(f"\n{name}")
    print("-" * 45)
    for key, value in row.items():
        print(f"{key}: {value}")

    print("\nTranspiled circuit:")
    print(compiled.draw(output="text", fold=100))

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"\nSaved comparison to: {OUT.relative_to(ROOT)}")
print("These are transpilation metrics, not hardware measurements.")

