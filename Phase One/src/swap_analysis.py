
# PRACTICE ONLY — NOT OFFICIAL HACKATHON DATA
# Compare QAOA SWAP overhead on two illustrative architectures

from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap

# Practice weighted Max-Cut graph
edges = [
    (0, 1, 3),
    (0, 2, 2),
    (1, 2, 1),
    (1, 3, 4),
    (2, 4, 2),
    (3, 4, 3),
]

n = 5
gamma = 0.5
beta = 0.3

# Build one-layer QAOA circuit
qc = QuantumCircuit(n)

for q in range(n):
    qc.h(q)

for u, v, weight in edges:
    qc.rzz(-gamma * weight, u, v)

for q in range(n):
    qc.rx(2 * beta, q)

# Two illustrative practice connectivity maps
linear_edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
ring_edges = linear_edges + [(4, 0)]

architectures = {
    "Practice A - Linear": linear_edges,
    "Practice B - Ring": ring_edges,
}

for name, connections in architectures.items():
    coupling = CouplingMap(couplinglist=connections)

    # Transpile using a two-qubit CX basis.
    # Do not pass a backend together with this custom coupling map.
    routed = transpile(
        qc,
        basis_gates=["rz", "sx", "x", "cx"],
        coupling_map=coupling,
        initial_layout=list(range(n)),
        routing_method="sabre",
        optimization_level=0,
        seed_transpiler=42,
    )

    ops = routed.count_ops()
        # SWAP gates may be decomposed into three CX gates.
    # Report explicit SWAPs separately from the total CX count.
    swap_count = ops.get("swap", 0)
    cx_count = ops.get("cx", 0)

    two_qubit_count = sum(
        count
        for gate, count in ops.items()
        if gate in ("cx", "cz", "ecr", "swap")
    )
    print("\n" + "=" * 40)
    print(name)
    print("SWAP gates:", swap_count)
    print("CX gates:", cx_count)
    print("Circuit depth:", routed.depth())
    print("Total gate count:", routed.size())
    print("Two-qubit gate count:", two_qubit_count)
    print("Gate counts:", ops)

    print("\nTranspiled circuit:")
   # Skip the large circuit diagram to avoid Windows encoding errors.

print("\nPractice comparison complete.")
print("These are illustrative architectures,")
print("not official hackathon processor measurements.")