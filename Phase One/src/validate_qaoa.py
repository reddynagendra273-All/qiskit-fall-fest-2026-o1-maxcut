
import csv
import json
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / "data" / "raw" / "maxcut_instances.json"
OPTIMA_PATH = ROOT / "results" / "tables" / "classical_optima.csv"

GAMMA = 0.1
BETA = 0.3
SHOTS = 2048
SEED = 42


def calculate_cut(bitstring, edges):
    bits = bitstring.replace(" ", "")[::-1]
    return sum(
        weight
        for u, v, weight in edges
        if bits[u] != bits[v]
    )


def main():
    with DATASET_PATH.open("r", encoding="utf-8-sig") as file:
        dataset = json.load(file)

    with OPTIMA_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        optima = {
            row["graph_id"]: int(row["classical_optimum"])
            for row in csv.DictReader(file)
        }

    simulator = AerSimulator()

    for graph in dataset["graphs"]:
        graph_id = graph["id"]
        edges = graph["edges"]
        n = dataset["num_vertices"]

        qc = QuantumCircuit(n, n)

        for q in range(n):
            qc.h(q)

        for u, v, weight in edges:
            qc.rzz(-GAMMA * weight, u, v)

        for q in range(n):
            qc.rx(2 * BETA, q)

        qc.measure(range(n), range(n))

        result = simulator.run(
            qc,
            shots=SHOTS,
            seed_simulator=SEED,
        ).result()

        counts = result.get_counts()
        cut_weights = {
            bits: calculate_cut(bits, edges)
            for bits in counts
        }

        average = sum(
            cut_weights[bits] * count
            for bits, count in counts.items()
        ) / SHOTS

        best_bitstring = max(
            cut_weights, key=cut_weights.get
        )
        best_cut = cut_weights[best_bitstring]
        optimum = optima[graph_id]

        print(f"\n{graph_id}")
        print("-" * 35)
        print(f"Gamma: {GAMMA}")
        print(f"Beta: {BETA}")
        print(f"Shots: {SHOTS}")
        print(f"Average cut weight: {average:.4f}")
        print(f"Best bitstring: {best_bitstring}")
        print(f"Best observed cut: {best_cut}")
        print(f"Classical optimum: {optimum}")
        print(f"Best sampled ratio: {best_cut / optimum:.4f}")
        print(
            "Validation:",
            "PASS" if best_cut <= optimum else "FAIL",
        )

        if best_cut > optimum:
            raise AssertionError(
                f"{graph_id}: sampled cut exceeds classical optimum"
            )

    print("\nQAOA validation completed.")
    print("AerSimulator results only; no hardware execution.")


if __name__ == "__main__":
    main()