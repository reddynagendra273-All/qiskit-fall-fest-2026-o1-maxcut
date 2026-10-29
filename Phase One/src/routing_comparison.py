# PRACTICE ONLY - NOT OFFICIAL HACKATHON DATA
"""Display recorded practice routing metrics from a CSV file."""

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_FILE = PROJECT_ROOT / "results" / "tables" / "routing_analysis_results.csv"


def main():
    if not RESULTS_FILE.exists():
        print(f"Results file not found: {RESULTS_FILE}")
        print("Run src/routing_analysis_v2.py first.")
        return

    with RESULTS_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        print("The routing results CSV is empty.")
        return

    print("PRACTICE ROUTING RESULTS")
    print("=" * 60)

    for row in rows:
        print("-" * 40)
        for key, value in row.items():
            print(f"{key}: {value}")

    print("\nPractice results only; not official hardware benchmarks.")


if __name__ == "__main__":
    main()
