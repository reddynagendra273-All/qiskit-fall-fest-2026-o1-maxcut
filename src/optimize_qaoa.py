
# PRACTICE ONLY — NOT OFFICIAL HACKATHON DATA
# Grid search for p=1 QAOA parameters on weighted Max-Cut

from itertools import product
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Practice graph: nodes A, B, C, D, E
edges = [
    (0, 1, 3),
    (0, 2, 2),
    (1, 2, 1),
    (1, 3, 4),
    (2, 4, 2),
    (3, 4, 3),
]

n = 5
shots = 10000
simulator = AerSimulator()

def cut_weight(bitstring):
    # Qiskit displays measured bitstrings in reverse qubit order.
    bits = bitstring[::-1]
    total = 0

    for u, v, weight in edges:
        if bits[u] != bits[v]:
            total += weight

    return total

def run_qaoa(gamma, beta):
    qc = QuantumCircuit(n, n)

    # Initial equal superposition
    for q in range(n):
        qc.h(q)

    # Problem unitary
    for u, v, weight in edges:
        qc.rzz(-gamma * weight, u, v)

    # Mixer unitary
    for q in range(n):
        qc.rx(2 * beta, q)

    qc.measure(range(n), range(n))

    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()

    average = sum(
        cut_weight(bits) * count
        for bits, count in counts.items()
    ) / shots

    best = max(cut_weight(bits) for bits in counts)

    return average, best

# Fine search around the best coarse-grid parameters
gammas = [i / 100 for i in range(20, 41, 2)]
betas = [i / 100 for i in range(30, 51, 2)]

results = []

for gamma, beta in product(gammas, betas):
    average, best = run_qaoa(gamma, beta)
    results.append((average, best, gamma, beta))

results.sort(reverse=True)

print("\nTOP 10 PARAMETER SETTINGS")
print("-" * 65)
print("Rank | Gamma | Beta | Average cut | Best observed cut")

for rank, (average, best, gamma, beta) in enumerate(results[:10], 1):
    print(
        f"{rank:4} | {gamma:5.2f} | {beta:4.2f} "
        f"| {average:11.3f} | {best:17}"
    )

print("\nKnown classical optimum: 13")
print("Search completed on a practice graph.")
print("Results are simulator estimates, not hardware results.")
