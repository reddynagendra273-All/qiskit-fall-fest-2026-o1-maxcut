import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for filename in ("processor_A.json", "processor_B.json"):
    path = ROOT / "processors" / filename

    with path.open("r", encoding="utf-8-sig") as f:
        processor = json.load(f)

    n = processor["num_qubits"]
    edges = processor["coupling_map"]

    assert n > 0, f"{filename}: invalid qubit count"

    for u, v in edges:
        assert 0 <= u < n and 0 <= v < n, (
            f"{filename}: edge {(u, v)} references an invalid qubit"
        )
        assert u != v, f"{filename}: self-coupling is invalid"

    print(f"\n{processor['processor_name']}")
    print("-" * 35)
    print(f"Qubits: {n}")
    print(f"Coupling edges: {len(edges)}")
    print(f"Can directly represent 6 graph vertices: {n >= 6}")
    print("Architecture validation: PASS")

print("\nNote: this validates architecture only, not hardware execution or noise.")
