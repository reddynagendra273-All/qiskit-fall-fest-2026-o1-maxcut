
import itertools
import networkx as nx
import matplotlib.pyplot as plt

# PRACTICE DATA ONLY â€” NOT OFFICIAL HACKATHON INPUT
edges = [
    ("A", "B", 3),
    ("A", "C", 2),
    ("B", "C", 1),
    ("B", "D", 4),
    ("C", "E", 2),
    ("D", "E", 3),
]

nodes = ["A", "B", "C", "D", "E"]

def calculate_cut(bits):
    """Calculate the total weight of edges crossing the cut."""
    side = dict(zip(nodes, bits))
    cut_weight = 0

    for u, v, weight in edges:
        if side[u] != side[v]:
            cut_weight += weight

    return cut_weight

# Test every possible assignment of nodes to two groups
best_weight = -1
best_assignment = None

for bits in itertools.product([0, 1], repeat=len(nodes)):
    weight = calculate_cut(bits)

    if weight > best_weight:
        best_weight = weight
        best_assignment = bits

group_0 = [nodes[i] for i, bit in enumerate(best_assignment) if bit == 0]
group_1 = [nodes[i] for i, bit in enumerate(best_assignment) if bit == 1]

print("PRACTICE MAX-CUT â€” CLASSICAL BASELINE")
print("-------------------------------------")
print("Group 0:", group_0)
print("Group 1:", group_1)
print("Maximum cut weight:", best_weight)

# Draw the practice graph
graph = nx.Graph()
graph.add_weighted_edges_from(edges)

colors = [
    "skyblue" if best_assignment[nodes.index(node)] == 0
    else "orange"
    for node in graph.nodes()
]

pos = nx.spring_layout(graph, seed=42)

nx.draw(
    graph, pos,
    with_labels=True,
    node_color=colors,
    node_size=1400,
    font_size=12,
    font_weight="bold"
)

nx.draw_networkx_edge_labels(
    graph, pos,
    edge_labels=nx.get_edge_attributes(graph, "weight")
)

plt.title("Practice Weighted Max-Cut â€” Classical Baseline")
plt.savefig("results/figures/maxcut_graph.png", dpi=300, bbox_inches="tight")
print("Graph saved as results/figures/maxcut_graph.png")
plt.close()
