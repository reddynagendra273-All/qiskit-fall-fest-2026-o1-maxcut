
import csv
import json
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    depolarizing_error,
    ReadoutError,
)

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "raw" / "maxcut_instances.json"
OUT_FILE = ROOT / "results" / "tables" / "noisy_processor_comparison_graph01.csv"

PROCESSORS = {
    "Processor B": ROOT / "processors" / "processor_B.json",
    "Processor D": ROOT / "processors" / "processor_D.json",
}

GAMMA = 0.1
BETA = 0.3
SHOTS = 4096
SEED = 42
BASIS_GATES = ["rz", "sx", "x", "cx"]


def load_json(path):
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def build_circuit(n, edges):
    circuit = QuantumCircuit(n)

    for q in range(n):
        circuit.h(q)

    for u, v, weight in edges:
        circuit.rzz(-GAMMA * weight, u, v)

    for q in range(n):
        circuit.rx(2 * BETA, q)

    circuit.measure_all()
    return circuit


def build_noise_model():
    noise = NoiseModel()

    noise.add_all_qubit_quantum_error(
        depolarizing_error(0.001, 1), ["rz", "sx", "x"]
    )
    noise.add_all_qubit_quantum_error(
        depolarizing_error(0.005, 2), ["cx"]
    )
    noise.add_all_qubit_readout_error(
        ReadoutError([[0.99, 0.01], [0.01, 0.99]])
    )
    return noise


def cut_value(bitstring, edges):
    bits = bitstring.replace(" ", "")[::-1]
    return sum(
        weight for u, v, weight in edges
        if bits[u] != bits[v]
    )


def main():
    dataset = load_json(DATA_FILE)
    graph = next(
        g for g in dataset["graphs"] if g["id"] == "graph_01"
    )
    n = dataset["num_vertices"]
    edges = [tuple(edge) for edge in graph["edges"]]
    circuit = build_circuit(n, edges)

    simulator = AerSimulator(
        noise_model=build_noise_model(),
        basis_gates=BASIS_GATES,
    )

    rows = []

    for name, config_path in PROCESSORS.items():
        config = load_json(config_path)
        coupling = CouplingMap(config["coupling_map"])

        compiled = transpile(
            circuit,
            basis_gates=BASIS_GATES,
            coupling_map=coupling,
            initial_layout=list(range(n)),
            optimization_level=1,
            seed_transpiler=SEED,
            routing_method="sabre",
        )

        result = simulator.run(
            compiled,
            shots=SHOTS,
            seed_simulator=SEED,
        ).result()

        counts = result.get_counts()
        scores = {bits: cut_value(bits, edges) for bits in counts}
        average_cut = sum(
            scores[bits] * count for bits, count in counts.items()
        ) / SHOTS
        best_cut = max(scores.values())
        optimal_shots = sum(
            count for bits, count in counts.items()
            if scores[bits] == 26
        )
        ops = compiled.count_ops()

        row = {
            "graph_id": "graph_01",
            "dataset_status": "team-created example; not official fixed graph",
            "processor": name,
            "physical_qubits_available": config["num_qubits"],
            "gamma": GAMMA,
            "beta": BETA,
            "shots": SHOTS,
            "single_qubit_depolarizing_p": 0.001,
            "cx_depolarizing_p": 0.005,
            "readout_bit_flip_p": 0.01,
            "transpiled_depth": compiled.depth(),
            "transpiled_total_gates": compiled.size(),
            "transpiled_cx_count": ops.get("cx", 0),
            "transpiled_explicit_swap_count": ops.get("swap", 0),
            "average_cut": average_cut,
            "best_sampled_cut": best_cut,
            "known_classical_optimum": 26,
            "optimal_sample_probability": optimal_shots / SHOTS,
            "status": "Noisy Aer simulation; not hardware execution",
        }
        rows.append(row)

        print(f"\n{name}")
        for key, value in row.items():
            print(f"{key}: {value}")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved comparison to: {OUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()