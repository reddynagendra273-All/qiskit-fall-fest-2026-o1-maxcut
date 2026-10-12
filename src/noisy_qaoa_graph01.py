
import csv
import json
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    depolarizing_error,
    ReadoutError,
)

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "raw" / "maxcut_instances.json"
OUT_FILE = ROOT / "results" / "tables" / "noisy_qaoa_graph01.csv"

GAMMA = 0.1
BETA = 0.3
SHOTS = 4096
SEED = 42
BASIS_GATES = ["rz", "sx", "x", "cx"]


def load_graph():
    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        dataset = json.load(file)

    for graph in dataset["graphs"]:
        if graph["id"] == "graph_01":
            return dataset["num_vertices"], graph["edges"]

    raise ValueError("graph_01 not found in dataset")


def build_circuit(num_qubits, edges):
    circuit = QuantumCircuit(num_qubits)

    for q in range(num_qubits):
        circuit.h(q)

    for u, v, weight in edges:
        circuit.rzz(-GAMMA * weight, u, v)

    for q in range(num_qubits):
        circuit.rx(2 * BETA, q)

    circuit.measure_all()
    return circuit


def build_noise_model():
    noise = NoiseModel()

    # Apply single-qubit depolarizing error to supported 1-qubit gates.
    one_qubit_error = depolarizing_error(0.001, 1)
    noise.add_all_qubit_quantum_error(
        one_qubit_error, ["rz", "sx", "x"]
    )

    # Apply the prescribed two-qubit error to CX gates.
    cx_error = depolarizing_error(0.005, 2)
    noise.add_all_qubit_quantum_error(cx_error, ["cx"])

    # Symmetric readout bit-flip error.
    readout_error = ReadoutError([
        [0.99, 0.01],
        [0.01, 0.99],
    ])
    noise.add_all_qubit_readout_error(readout_error)

    return noise


def cut_value(bitstring, edges):
    # Qiskit count strings list the highest-index classical bit first.
    bits = bitstring.replace(" ", "")[::-1]
    return sum(
        weight
        for u, v, weight in edges
        if bits[u] != bits[v]
    )


def main():
    num_qubits, edges = load_graph()
    circuit = build_circuit(num_qubits, edges)

    # Transpile first, then simulate using the same declared basis.
    compiled = transpile(
        circuit,
        basis_gates=BASIS_GATES,
        optimization_level=1,
        seed_transpiler=SEED,
    )

    simulator = AerSimulator(
        noise_model=build_noise_model(),
        basis_gates=BASIS_GATES,
    )
    result = simulator.run(
        compiled,
        shots=SHOTS,
        seed_simulator=SEED,
    ).result()

    counts = result.get_counts()
    total_weight = sum(weight for _, _, weight in edges)
    cut_scores = {
        bits: cut_value(bits, edges)
        for bits in counts
    }

    average_cut = sum(
        cut_scores[bits] * count
        for bits, count in counts.items()
    ) / SHOTS

    best_sampled_cut = max(cut_scores.values())
    optimal_count = sum(
        count
        for bits, count in counts.items()
        if cut_scores[bits] == 26
    )

    row = {
        "graph_id": "graph_01",
        "dataset_status": "team-created example; not official fixed graph",
        "gamma": GAMMA,
        "beta": BETA,
        "shots": SHOTS,
        "single_qubit_depolarizing_p": 0.001,
        "cx_depolarizing_p": 0.005,
        "readout_bit_flip_p": 0.01,
        "transpiled_depth": compiled.depth(),
        "transpiled_total_gates": compiled.size(),
        "transpiled_cx_count": compiled.count_ops().get("cx", 0),
        "average_cut": average_cut,
        "best_sampled_cut": best_sampled_cut,
        "known_classical_optimum": 26,
        "optimal_sample_probability": optimal_count / SHOTS,
        "shots": SHOTS,
        "status": (
            "Noisy Aer simulation; prescribed gate/readout error rates; "
            "not hardware execution"
        ),
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)

    for key, value in row.items():
        print(f"{key}: {value}")

    print(f"\nSaved noisy results to: {OUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
