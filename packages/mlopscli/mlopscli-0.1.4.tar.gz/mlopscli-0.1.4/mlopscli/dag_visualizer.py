# mlopscli/dag_visualizer.py
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from mlopscli.constants import ARTIFACTS_DIRECTORY


def visualize_dag(pipeline_name: str, steps: dict, output_path=None):
    if output_path is None:
        output_path = f"{ARTIFACTS_DIRECTORY}/{pipeline_name}_dag.png"

    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    G = nx.DiGraph()

    for step_name, step_info in steps.items():
        G.add_node(step_name)
        for dep in step_info.get("depends_on", []):
            G.add_edge(dep, step_name)

    # Use spring layout for a more natural-looking DAG
    pos = nx.spring_layout(G, k=1.2, iterations=100, seed=42)

    plt.figure(figsize=(2.5 * len(steps), 3))
    nx.draw(
        G,
        pos,
        with_labels=True,
        arrows=True,
        node_color="lightgreen",
        node_size=2200,
        font_size=11,
        edge_color="gray",
        arrowstyle="-|>",
        arrowsize=20,
    )

    plt.title(f"{pipeline_name} DAG", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"📈 DAG saved to: {output_path}")
