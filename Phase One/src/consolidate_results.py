
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "tables"


def read_csv(filename):
    path = RESULTS / filename
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(filename, rows):
    if not rows:
        print(f"No rows to write for {filename}")
        return

    path = RESULTS / filename
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved: {path.relative_to(ROOT)}")


def main():
    classical = {
        row["graph_id"]: row
        for row in read_csv("classical_optima.csv")
    }

    optimization = {
        row["graph_id"]: row
        for row in read_csv("qaoa_optimization.csv")
    }

    routing = read_csv("processor_routing_comparison.csv")

    routing_by_key = {
        (row["graph_id"], row["processor"]): row
        for row in routing
    }

    rows = []

    for graph_id in sorted(classical):
        opt = classical[graph_id]
        qaoa = optimization.get(graph_id, {})

        processor_a = routing_by_key.get(
            (graph_id, "Processor A"), {}
        )
        processor_b = routing_by_key.get(
            (graph_id, "Processor B"), {}
        )

        rows.append({
            "graph_id": graph_id,
            "classical_optimum": opt.get("classical_optimum", ""),
            "optimal_bitstring": opt.get(
                "one_optimal_bitstring_mask_order", ""
            ),
            "optimal_assignments_count": opt.get(
                "optimal_assignments_count", ""
            ),
            "qaoa_gamma": qaoa.get("gamma", ""),
            "qaoa_beta": qaoa.get("beta", ""),
            "qaoa_shots": qaoa.get("shots", ""),
            "qaoa_best_sampled_cut": qaoa.get(
                "best_sampled_cut", ""
            ),
            "qaoa_average_cut": qaoa.get("average_cut", ""),
            "qaoa_average_approximation_ratio": qaoa.get(
                "average_approximation_ratio", ""
            ),
            "qaoa_best_sampled_approximation_ratio": qaoa.get(
                "best_sampled_approximation_ratio", ""
            ),
            "qaoa_optimal_cut_probability": qaoa.get(
                "optimal_cut_probability", ""
            ),
            "processor_a_mapping_feasible": processor_a.get(
                "mapping_feasible", ""
            ),
            "processor_b_mapping_feasible": processor_b.get(
                "mapping_feasible", ""
            ),
            "processor_b_depth": processor_b.get("depth", ""),
            "processor_b_total_gates": processor_b.get(
                "total_gates", ""
            ),
            "processor_b_cx_count": processor_b.get("cx_count", ""),
            "processor_b_explicit_swap_count": processor_b.get(
                "explicit_swap_count", ""
            ),
            "measurement_note": (
                "QAOA simulator and ideal transpilation; "
                "not hardware measurements"
            )
        })

    write_csv("consolidated_benchmark.csv", rows)

    print("\nConsolidated benchmark summary")
    for row in rows:
        print(
            f'{row["graph_id"]}: '
            f'optimum={row["classical_optimum"]}, '
            f'QAOA average={row["qaoa_average_cut"]}, '
            f'ratio={row["qaoa_average_approximation_ratio"]}, '
            f'Processor B depth={row["processor_b_depth"]}, '
            f'CX={row["processor_b_cx_count"]}'
        )


if __name__ == "__main__":
    main()