import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "raw" / "maxcut_instances.json"
OUTPUT = ROOT / "results" / "tables" / "classical_optima.csv"

with INPUT.open("r", encoding="utf-8-sig") as f:
    dataset = json.load(f)

n = dataset["num_vertices"]
results = []

for graph in dataset["graphs"]:
    edges = graph["edges"]

    # Validate every edge before evaluating it.
    for u, v, weight in edges:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError(f"{graph['id']}: invalid vertex in edge {(u, v, weight)}")
        if u == v:
            raise ValueError(f"{graph['id']}: self-loops are not supported")
        if not isinstance(weight, int) or not 1 <= weight <= 5:
            raise ValueError(f"{graph['id']}: invalid edge weight {weight}")

    best_weight = -1
    best_bits = None
    optimal_count = 0

    # Check all 2^n assignments.
    for mask in range(1 << n):
        bits = format(mask, f"0{n}b")
        cut_weight = sum(
            weight
            for u, v, weight in edges
            if ((mask >> u) & 1) != ((mask >> v) & 1)
        )

        if cut_weight > best_weight:
            best_weight = cut_weight
            best_bits = bits
            optimal_count = 1
        elif cut_weight == best_weight:
            optimal_count += 1

    side_0 = [i for i in range(n) if best_bits[n - 1 - i] == "0"]
    side_1 = [i for i in range(n) if best_bits[n - 1 - i] == "1"]

    results.append({
        "graph_id": graph["id"],
        "num_vertices": n,
        "num_edges": len(edges),
        "classical_optimum": best_weight,
        "one_optimal_bitstring_mask_order": best_bits,
        "optimal_assignments_count": optimal_count,
        "side_0_vertices": " ".join(map(str, side_0)),
        "side_1_vertices": " ".join(map(str, side_1)),
        "assignments_checked": 1 << n,
    })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\nCLASSICAL MAX-CUT RESULTS")
print("=" * 65)

for row in results:
    print(f"\nGraph: {row['graph_id']}")
    print(f"Edges: {row['num_edges']}")
    print(f"Exact optimum: {row['classical_optimum']}")
    print(f"One optimal bitstring: {row['one_optimal_bitstring_mask_order']}")
    print(f"Optimal assignments: {row['optimal_assignments_count']}")
    print(f"Assignments checked: {row['assignments_checked']}")

print(f"\nSaved results to: {OUTPUT.relative_to(ROOT)}")
