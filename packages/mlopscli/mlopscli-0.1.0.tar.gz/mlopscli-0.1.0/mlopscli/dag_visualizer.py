# mlopscli/dag_visualizer.py
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path


def visualize_dag(pipeline_name: str, steps: dict, output_path=None):
    # Set default output path
    if output_path is None:
        output_path = f"mlops_artifacts/{pipeline_name}_dag.png"

    # Ensure artifacts folder exists
    artifacts_dir = Path(output_path).parent
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    G = nx.DiGraph()

    # Add nodes and edges
    for step_name, step_info in steps.items():
        G.add_node(step_name)
        for dep in step_info.get("depends_on", []):
            G.add_edge(dep, step_name)

    # Simple linear topological sort to arrange nodes
    ordered_steps = list(nx.topological_sort(G))
    pos = {
        step: (i, 0) for i, step in enumerate(ordered_steps)
    }  # x=i, y=0 for horizontal layout

    plt.figure(figsize=(2.5 * len(steps), 2.5))
    nx.draw(
        G,
        pos,
        with_labels=True,
        arrows=True,
        node_color="lightgreen",
        node_size=2200,
        font_size=11,
        edge_color="gray",
    )

    plt.title(f"{pipeline_name} DAG", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"📈 DAG saved to: {output_path}")
