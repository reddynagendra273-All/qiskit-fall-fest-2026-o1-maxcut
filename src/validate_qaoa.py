
# PRACTICE ONLY — NOT OFFICIAL HACKATHON DATA
# Validate the best p=1 QAOA parameters

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

edges = [
    (0, 1, 3),
    (0, 2, 2),
    (1, 2, 1),
    (1, 3, 4),
    (2, 4, 2),
    (3, 4, 3),
]

n = 5
gamma = 0.26
beta = 0.42
shots = 10000

simulator = AerSimulator()

def cut_weight(bitstring):
    bits = bitstring[::-1]
    return sum(
        weight
        for u, v, weight in edges
        if bits[u] != bits[v]
    )

qc = QuantumCircuit(n, n)

for q in range(n):
    qc.h(q)

for u, v, weight in edges:
    qc.rzz(-gamma * weight, u, v)

for q in range(n):
    qc.rx(2 * beta, q)

qc.measure(range(n), range(n))

result = simulator.run(
    qc,
    shots=shots,
    seed_simulator=42
).result()

counts = result.get_counts()

average = sum(
    cut_weight(bits) * count
    for bits, count in counts.items()
) / shots

best_bitstring = max(counts, key=lambda bits: cut_weight(bits))
best_cut = cut_weight(best_bitstring)

print("PRACTICE QAOA VALIDATION")
print("-" * 35)
print(f"Gamma: {gamma}")
print(f"Beta: {beta}")
print(f"Shots: {shots}")
print(f"Average cut weight: {average:.3f}")
print(f"Best bitstring: {best_bitstring}")
print(f"Best observed cut: {best_cut}")
print("Classical optimum: 13")
print("Practice simulator results only.")
