
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "tables" / "consolidated_benchmark.csv"
FIGURES = ROOT / "results" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RESULTS)

# Graph 1: QAOA performance
plt.figure(figsize=(8, 5))
plt.bar(df["graph_id"], df["qaoa_average_approximation_ratio"])
plt.axhline(1.0, linestyle="--", label="Classical optimum")
plt.ylabel("Average approximation ratio")
plt.xlabel("Graph")
plt.title("QAOA Performance on Max-Cut Graphs")
plt.ylim(0, 1.1)
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "qaoa_approximation_ratios.png", dpi=300)
plt.close()

# Graph 2: Processor B circuit cost
plt.figure(figsize=(8, 5))
x = range(len(df))
width = 0.35

plt.bar(
    [i - width / 2 for i in x],
    df["processor_b_depth"],
    width,
    label="Circuit depth",
)
plt.bar(
    [i + width / 2 for i in x],
    df["processor_b_cx_count"],
    width,
    label="CX gate count",
)
plt.xticks(list(x), df["graph_id"])
plt.ylabel("Count")
plt.xlabel("Graph")
plt.title("Processor B Circuit Cost")
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "processor_b_circuit_cost.png", dpi=300)
plt.close()

print("Success! Both graphs have been saved.")
print(FIGURES)