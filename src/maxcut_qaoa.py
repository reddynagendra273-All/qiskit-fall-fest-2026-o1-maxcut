
# PRACTICE PROJECT ONLY — NOT OFFICIAL HACKATHON DATA
# QAOA for Weighted Max-Cut using Qiskit

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Practice graph: (node 1, node 2, edge weight)
edges = [
    (0, 1, 3),
    (0, 2, 2),
    (1, 2, 1),
    (1, 3, 4),
    (2, 4, 2),
    (3, 4, 3),
]

num_qubits = 5

# QAOA parameters for a simple first experiment
gamma = 0.5
beta = 0.3
shots = 2048

qc = QuantumCircuit(num_qubits, num_qubits)

# 1. Create an equal superposition of all bitstrings
for qubit in range(num_qubits):
    qc.h(qubit)

# 2. Cost unitary for weighted Max-Cut
for u, v, weight in edges:
    qc.rzz(-gamma * weight, u, v)

# 3. Mixing unitary
for qubit in range(num_qubits):
    qc.rx(2 * beta, qubit)

# 4. Measure every qubit
qc.measure(range(num_qubits), range(num_qubits))

print("QAOA circuit created successfully!")
print("Number of qubits:", num_qubits)
print("Number of QAOA layers: 1")
print("\nCircuit:")
print(qc.draw(output="text"))

# 5. Run the circuit on a local simulator
simulator = AerSimulator()
compiled_qc = transpile(qc, simulator, optimization_level=0)
# Circuit resource analysis
print("\n--- CIRCUIT RESOURCE ANALYSIS ---")
print("Total circuit depth:", compiled_qc.depth())
print("Total gate count:", compiled_qc.size())
print("Gate counts:", compiled_qc.count_ops())

two_qubit_gates = {"rzz", "cx", "cz", "ecr", "swap"}

two_qubit_count = sum(
    count
    for gate, count in compiled_qc.count_ops().items()
    if gate in two_qubit_gates
)

print("Two-qubit gate count:", two_qubit_count)
result = simulator.run(compiled_qc, shots=shots).result()
counts = result.get_counts()

# 6. Calculate the cut weight for a measured bitstring
def calculate_cut(bitstring):
    # Qiskit displays classical bits in reverse order
    bits = bitstring.replace(" ", "")[::-1]

    total = 0
    for u, v, weight in edges:
        if bits[u] != bits[v]:
            total += weight

    return total

# 7. Find the best sampled solution
best_bitstring = max(counts, key=lambda b: calculate_cut(b))
best_weight = calculate_cut(best_bitstring)

# 8. Calculate the average cut weight over all measurements
average_weight = sum(
    calculate_cut(bits) * count
    for bits, count in counts.items()
) / shots

print("\n--- QAOA PRACTICE RESULTS ---")
print("Shots:", shots)
print("Best measured bitstring:", best_bitstring)
print("Best sampled cut weight:", best_weight)
print("Average cut weight:", round(average_weight, 3))
print("Classical optimum for this practice graph: 13")
print("\nNote: This is a single-layer QAOA experiment")
print("with fixed parameters, not an optimized QAOA result.")