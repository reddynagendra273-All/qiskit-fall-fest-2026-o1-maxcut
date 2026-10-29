import json
import random
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "raw" / "official_maxcut_instance.json"

if OUTPUT.exists():
    raise FileExistsError(
        f"Refusing to overwrite existing official instance: {OUTPUT}"
    )

GRAPH_SEED = 42
WEIGHT_SEED = 42  # Reproducibility choice; the guide does not specify this seed.

graph = nx.erdos_renyi_graph(n=6, p=0.5, seed=GRAPH_SEED)
weight_rng = random.Random(WEIGHT_SEED)

edges = [
    [int(u), int(v), weight_rng.randint(1, 5)]
    for u, v in sorted(graph.edges())
]

instance = {
    "dataset_name": "Qiskit Fall Fest 2026 Phase 1 PS-O1 Official Instance",
    "source": "Graph generated with the parameters specified in the Phase 1 guide",
    "graph_generation": {
        "method": "networkx.erdos_renyi_graph",
        "n": 6,
        "p": 0.5,
        "seed": GRAPH_SEED,
    },
    "weight_assignment": {
        "method": "Python random.Random().randint(1, 5)",
        "seed": WEIGHT_SEED,
        "note": "Weight seed is a documented reproducibility choice, not a guide-specified requirement.",
    },
    "num_vertices": 6,
    "graphs": [
        {
            "id": "official_graph_01",
            "edges": edges,
        }
    ],
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(instance, indent=2) + "\n", encoding="utf-8")

print(f"Created: {OUTPUT.relative_to(ROOT)}")
print(f"Vertices: {graph.number_of_nodes()}")
print(f"Edges: {graph.number_of_edges()}")
print(f"Weighted edges: {edges}")
