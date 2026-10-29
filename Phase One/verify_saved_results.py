
import json
from pathlib import Path

path = Path("phase-2-maxcut/phase2_results.json")
data = json.loads(path.read_text(encoding="utf-8-sig"))

edges = data["weighted_edges"]
optimal_strings = set(data["optimal_bitstrings_x0_to_xn"])

def cut_weight(bitstring):
    bits = bitstring[::-1]
    total = 0
    for u, v, weight in edges:
        if bits[int(u)] != bits[int(v)]:
            total += float(weight)
    return total
print("Independent recomputation")
print("-" * 50)

for result in data["processor_results"]:
    if not result.get("executable"):
        continue

    counts = result["counts"]
    shots = sum(counts.values())

    mean_cut = sum(
        count * cut_weight(bits)
        for bits, count in counts.items()
    ) / shots

    p_opt = sum(
        count for bits, count in counts.items()
        if bits in optimal_strings
    ) / shots

    mean_match = abs(mean_cut - result["mean_cut"]) < 1e-8
    popt_match = abs(p_opt - result["p_opt"]) < 1e-8

    print(f"\n{result['processor']} - {result['condition']}")
    print("Shots:", shots)
    print(f"Mean cut: {mean_cut:.8f}")
    print(f"Saved mean: {result['mean_cut']:.8f}")
    print(f"P_opt: {p_opt:.8f}")
    print(f"Saved P_opt: {result['p_opt']:.8f}")
    print("Match:", mean_match and popt_match)
