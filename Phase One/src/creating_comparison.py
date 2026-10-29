
# PRACTICE ONLY — NOT OFFICIAL HACKATHON DATA
# Compare QAOA circuit metrics under different connectivity constraints

from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap

n = 5
gamma = 0.26
beta = 0.42

edges = [
    (0, 1, 3),
    (0, 2, 2),
    (1, 2, 1),
    (1, 3, 4),
    (2, 4, 2),
    (3, 4, 3),
]

def build_qaoa():
    qc = QuantumCircuit(n)

    for q in range(n):
        qc.h(q)

    for u, v, weight in edges:
        qc.rzz(-gamma * weight, u, v)

    for q in range(n):
        qc.rx(2 * beta, q)

    return qc

base = build_qaoa()

# Use a common basis so the gate counts can be compared.
basis = ["rz", "sx", "x", "cx"]

linear_edges = [
    (0, 1), (1, 2), (2, 3), (3, 4)
]

ring_edges = linear_edges + [(4, 0)]

configs = [
    ("Unrestricted", None),
    ("Practice Linear", CouplingMap(couplinglist=linear_edges)),
    ("Practice Ring", CouplingMap(couplinglist=ring_edges)),
]

print("QAOA ROUTING COMPARISON")
print("=" * 65)

for name, coupling in configs:
    options = {
        "basis_gates": basis,
        "optimization_level": 0,
        "seed_transpiler": 42,
    }

    if coupling is not None:
        options["coupling_map"] = coupling
        options["initial_layout"] = list(range(n))
        options["routing_method"] = "sabre"

    routed = transpile(base, **options)
    counts = routed.count_ops()

    cx_count = counts.get("cx", 0)
    swap_count = counts.get("swap", 0)
    two_qubit_gates = {"cx", "swap", "cz", "ecr", "rzz"}
    two_qubit_count = sum(
        count
        for gate, count in counts.items()
        if gate in two_qubit_gates
    )
    print(f"\n{name}")
    print("-" * 40)
    print(f"Depth: {routed.depth()}")
    print(f"Total gates: {routed.size()}")
    print(f"CX gates: {cx_count}")
    print(f"Explicit SWAP gates: {swap_count}")
    print(f"Two-qubit gates (CX/SWAP/CZ): {two_qubit_count}")
    print(f"Operations: {dict(counts)}")

print("\nPractice comparison only; no hardware execution.")
