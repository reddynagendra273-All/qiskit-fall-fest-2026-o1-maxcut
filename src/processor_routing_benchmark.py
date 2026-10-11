
import csv
import json
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "raw" / "maxcut_instances.json"
OUT = ROOT / "results" / "tables" / "processor_routing_comparison.csv"

PROCESSOR_FILES = {
    "Processor A": ROOT / "processors" / "processor_A.json",
    "Processor B": ROOT / "processors" / "processor_B.json",
}

GAMMA = 0.1
BETA = 0.3
BASIS_GATES = ["rz", "sx", "x", "cx"]
SEED = 42


def load_json(path):
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def build_qaoa_circuit(num_vertices, edges):
    """Build a p=1 Max-Cut QAOA circuit."""
    circuit = QuantumCircuit(num_vertices)

    for qubit in range(num_vertices):
        circuit.h(qubit)

    for u, v, weight in edges:
        circuit.rzz(-GAMMA * weight, u, v)

    for qubit in range(num_vertices):
        circuit.rx(2 * BETA, qubit)

    return circuit


def main():
    dataset = load_json(DATA_FILE)
    processors = {
        name: load_json(path)
        for name, path in PROCESSOR_FILES.items()
    }

    rows = []

    for graph in dataset["graphs"]:
        graph_id = graph["id"]
        num_vertices = dataset["num_vertices"]
        edges = [tuple(edge) for edge in graph["edges"]]
        circuit = build_qaoa_circuit(num_vertices, edges)

        print(f"\nGraph: {graph_id}")
        print(f"Logical vertices: {num_vertices}")
        print(f"Weighted edges: {len(edges)}")

        for name, config in processors.items():
            available = config["num_qubits"]

            row = {
                "graph_id": graph_id,
                "processor": name,
                "logical_qubits_required": num_vertices,
                "physical_qubits_available": available,
                "coupling_edges": len(config["coupling_map"]),
                "gamma": GAMMA,
                "beta": BETA,
                "basis_gates": ",".join(BASIS_GATES),
            }

            if available < num_vertices:
                row.update({
                    "mapping_feasible": False,
                    "depth": "",
                    "total_gates": "",
                    "cx_count": "",
                    "explicit_swap_count": "",
                    "status": (
                        "infeasible: insufficient physical qubits "
                        "for direct six-qubit mapping"
                    ),
                })
                print(f"{name}: infeasible for direct mapping")
                rows.append(row)
                continue

            coupling = CouplingMap(config["coupling_map"])

            try:
                compiled = transpile(
                    circuit,
                    basis_gates=BASIS_GATES,
                    coupling_map=coupling,
                    initial_layout=list(range(num_vertices)),
                    optimization_level=3,
                    seed_transpiler=SEED,
                )

                operations = compiled.count_ops()

                row.update({
                    "mapping_feasible": True,
                    "depth": compiled.depth(),
                    "total_gates": compiled.size(),
                    "cx_count": operations.get("cx", 0),
                    "explicit_swap_count": operations.get("swap", 0),
                    "status": (
                        "ideal transpilation only; "
                        "not hardware execution"
                    ),
                })

                print(
                    f"{name}: depth={compiled.depth()}, "
                    f"CX={operations.get('cx', 0)}, "
                    f"SWAP={operations.get('swap', 0)}"
                )

            except Exception as error:
                row.update({
                    "mapping_feasible": False,
                    "depth": "",
                    "total_gates": "",
                    "cx_count": "",
                    "explicit_swap_count": "",
                    "status": f"transpilation failed: {error}",
                })
                print(f"{name}: transpilation failed: {error}")

            rows.append(row)

    OUT.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0].keys())
    with OUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved results to: {OUT.relative_to(ROOT)}")
    print("All results are transpilation metrics, not hardware measurements.")


if __name__ == "__main__":
    main()