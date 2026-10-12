
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_LOGICAL_QUBITS = 6


def main():
    for filename in ("processor_A.json", "processor_B.json"):
        path = ROOT / "processors" / filename

        with path.open("r", encoding="utf-8-sig") as file:
            processor = json.load(file)

        num_qubits = processor["num_qubits"]
        coupling_map = processor["coupling_map"]
        processor_name = processor["processor_name"]

        assert num_qubits > 0, (
            f"{filename}: invalid qubit count"
        )

        for u, v in coupling_map:
            assert 0 <= u < num_qubits and 0 <= v < num_qubits, (
                f"{filename}: invalid coupling edge {(u, v)}"
            )
            assert u != v, (
                f"{filename}: self-coupling is invalid"
            )

        mapping_feasible = num_qubits >= REQUIRED_LOGICAL_QUBITS

        print(f"\n{processor_name}")
        print("-" * 35)
        print(f"Physical qubits: {num_qubits}")
        print(f"Coupling edges: {len(coupling_map)}")
        print(
            f"Six-vertex direct mapping: "
            f"{'FEASIBLE' if mapping_feasible else 'INFEASIBLE'}"
        )
        print("Architecture validation: PASS")

    print(
        "\nNote: this checks qubit count and coupling-map indices only."
    )
    print(
        "It does not validate hardware noise or hardware execution."
    )


if __name__ == "__main__":
    main()