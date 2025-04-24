import sys
import contextlib
import numpy as np
import pandas as pd
import seaborn as sns
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from IPython.display import display
from pgmpy.models import BayesianNetwork, DiscreteBayesianNetwork
from bibas.inference_utils import compute_bibas_pairwise, rank_sources_for_target


def plot_binary_bibas_heatmap(model, operation="observe", filename=None, title=None):
    """
    Plots a heatmap showing the BIBAS score from each source variable to each target variable
    in a fully binary Bayesian Network.

    Parameters:
        model: DiscreteBayesianNetwork – a BN with only binary variables
        operation: str – 'observe' (default) uses evidence; 'do' uses intervention (do-calculus)
        filename: str – if provided, saves the plot to file (PNG)
        title: str – optional custom title for the heatmap
    """
    nodes = sorted(model.nodes())

    # Validate that all variables in the network are binary
    for node in nodes:
        cpd = model.get_cpds(node)
        if cpd.variable_card != 2:
            raise ValueError(f"All nodes must be binary. Node '{node}' has {cpd.variable_card} states.")

    # Compute the BIBAS score from each source node to each target node
    bibas_matrix = pd.DataFrame(index=nodes, columns=nodes)
    for src in nodes:
        for tgt in nodes:
            if src == tgt:
                bibas_matrix.loc[src, tgt] = np.nan  # self-impact is visually excluded
            else:
                try:
                    score = compute_bibas_pairwise(model, src, tgt, target_positive_state=1, operation=operation)
                    bibas_matrix.loc[src, tgt] = 0.0 if score is None else score  # treat invalid/undefined as 0
                except:
                    bibas_matrix.loc[src, tgt] = 0.0  # fallback in case of any inference error

    bibas_matrix = bibas_matrix.astype(float)

    # Create the heatmap
    n = len(nodes)
    fig, ax = plt.subplots(figsize=(1.2 * n, 1.1 * n))
    sns.heatmap(
        bibas_matrix,
        annot=True,             # show score values in cells
        fmt=".1f",              # one decimal point
        cmap='Reds',            # white to red gradient
        square=True,
        linewidths=0.5,
        linecolor='white',
        mask=np.eye(n, dtype=bool),  # mask diagonal
        cbar_kws={"label": "BIBAS Score", "shrink": 0.6},
        ax=ax
    )

    # Add hatched rectangles on the diagonal to visually indicate self-impact is excluded
    for i in range(n):
        rect = patches.Rectangle((i, i), 1, 1, hatch='///',
                                 fill=False, edgecolor='gray', linewidth=0)
        ax.add_patch(rect)

    # Add title and labels
    ax.set_title(title or f"BIBAS Factor (operation = '{operation}')", fontsize=14)
    ax.set_xlabel("Target Node")
    ax.set_ylabel("Source Node")
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    plt.tight_layout()

    # Output: either save to file or display interactively
    if filename:
        plt.savefig(filename, bbox_inches="tight", dpi=300)
        plt.close()
    else:
        with contextlib.redirect_stderr(sys.__stdout__):
            plt.show()


def plot_ranked_sources_for_target(model, target, target_positive_state=1, operation="observe", filename=None, title=None):
    """
    Plot a horizontal bar chart ranking all sources by their BIBAS impact on a given binary target.

    Parameters:
        model: pgmpy Bayesian Network
        target: str – target node (must be binary)
        target_positive_state: int – which state is considered "positive"
        operation: 'observe' or 'do'
        filename: str – optional path to save the plot
        title: str – optional custom plot title
    """
    try:
        df = rank_sources_for_target(model, target, target_positive_state, operation)

        plt.figure(figsize=(10, 0.5 * len(df)))
        sns.barplot(data=df, x="bibas_score", y="source", hue="source", palette="Reds_r", legend=False)

        plt.xlabel("BIBAS Score")
        plt.ylabel("Source Node")
        plt.title(title or f"BIBAS Ranking on Target: '{target}' (operation = '{operation}')")

        # Annotate bars with values
        for i, row in df.iterrows():
            plt.text(row.bibas_score + 0.5, i, f"{row.bibas_score:.1f}", va='center')

        plt.xlim(0, df["bibas_score"].max() * 1.1)
        plt.tight_layout()

        if filename:
            plt.savefig(filename, bbox_inches="tight", dpi=300)
            plt.close()
        else:
            with contextlib.redirect_stderr(sys.__stdout__):
                plt.show()

    except Exception as e:
        print(f"[BIBAS Error] {e}")


def plot_bn(model, layout=nx.spring_layout, type="none", target=None, operation="observe", filename=None, title=None):
    """
    Plot a Bayesian Network with optional BIBAS-based node/edge analysis.

    Parameters:
        model: pgmpy.models.DiscreteBayesianNetwork
        layout: function
        type: str
        target: str (optional)
        operation: str
        filename: str (optional)
        title: str (optional)
    """
    if not isinstance(model, DiscreteBayesianNetwork):
        raise ValueError("Input must be a pgmpy DiscreteBayesianNetwork.")

    nodes = sorted(model.nodes())
    edges = model.edges()
    G = nx.DiGraph(edges)
    pos = layout(G, seed=42)

    def is_binary(node):
        return model.get_cpds(node).variable_card == 2

    if type in ['edges', 'edges_and_impacts']:
        non_binary_nodes = [n for n in nodes if not is_binary(n)]
        if non_binary_nodes:
            raise ValueError(f"Edge-based visualization requires all nodes to be binary. Non-binary: {non_binary_nodes}")

    node_colors = {}
    edge_colors = {}
    edge_labels = {}
    node_labels = {n: n for n in nodes}

    if type == "none":
        node_colors = {n: "skyblue" for n in nodes}

    elif type == "blanket":
        if not target:
            raise ValueError("Target must be specified for type='blanket'")
        blanket = set(model.get_markov_blanket(target))
        for node in nodes:
            if node == target:
                node_colors[node] = "lightgreen"
            elif node in blanket:
                node_colors[node] = "salmon"
            else:
                node_colors[node] = "skyblue"

    elif type == "impacts":
        if not target:
            raise ValueError("Target must be specified for type='impacts'")
        bibas_scores = {
            node: compute_bibas_pairwise(model, node, target, operation=operation)
            if node != target else None
            for node in nodes
        }
        valid_scores = [v for v in bibas_scores.values() if v is not None]
        min_score, max_score = min(valid_scores), max(valid_scores)

        for node in nodes:
            if node == target:
                node_colors[node] = "lightgreen"
            else:
                score = bibas_scores[node]
                norm = (score - min_score) / (max_score - min_score) if max_score > min_score else 0
                intensity = 0.2 + norm * 0.6
                node_colors[node] = (1, 1 - intensity, 1 - intensity)
                node_labels[node] = f"{node}\n{score:.2f}"

    elif type == "edges":
        scores = []
        for (src, tgt) in edges:
            score = compute_bibas_pairwise(model, src, tgt, operation=operation)
            scores.append(score)
            edge_labels[(src, tgt)] = f"{score:.1f}"

        min_score, max_score = min(scores), max(scores)
        for (src, tgt), score in zip(edges, scores):
            norm = (score - min_score) / (max_score - min_score) if max_score > min_score else 0
            intensity = 0.2 + norm * 0.6
            edge_colors[(src, tgt)] = (1, 1 - intensity, 1 - intensity)

        node_colors = {n: "skyblue" for n in nodes}

    elif type == "edges_and_impacts":
        if not target:
            raise ValueError("Target must be specified for type='edges_and_impacts'")

        # Node impacts
        bibas_scores = {
            node: compute_bibas_pairwise(model, node, target, operation=operation)
            if node != target else None
            for node in nodes
        }
        valid_node_scores = [v for v in bibas_scores.values() if v is not None]
        min_node, max_node = min(valid_node_scores), max(valid_node_scores)

        for node in nodes:
            if node == target:
                node_colors[node] = "lightgreen"
            else:
                score = bibas_scores[node]
                norm = (score - min_node) / (max_node - min_node) if max_node > min_node else 0
                intensity = 0.2 + norm * 0.6
                node_colors[node] = (1, 1 - intensity, 1 - intensity)
                node_labels[node] = f"{node}\n{score:.2f}"

        # Edge impacts
        edge_scores = []
        for (src, tgt) in edges:
            score = compute_bibas_pairwise(model, src, tgt, operation=operation)
            edge_labels[(src, tgt)] = f"{score:.1f}"
            edge_scores.append(score)

        min_edge, max_edge = min(edge_scores), max(edge_scores)
        for (src, tgt), score in zip(edges, edge_scores):
            norm = (score - min_edge) / (max_edge - min_edge) if max_edge > min_edge else 0
            intensity = 0.2 + norm * 0.6
            edge_colors[(src, tgt)] = (1, 1 - intensity, 1 - intensity)

    else:
        raise ValueError(f"Unknown type: '{type}'. Valid options: none, blanket, impacts, edges, edges_and_impacts.")

    fig, ax = plt.subplots(figsize=(1.2 * len(nodes), 1.2 * len(nodes)))

    nx.draw_networkx_nodes(G, pos, node_color=[node_colors.get(n, "gray") for n in G.nodes()], node_size=1500, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, ax=ax)

    if type in ["edges", "edges_and_impacts"]:
        edge_list = list(edge_colors.keys())
        edge_color_vals = list(edge_colors.values())
        nx.draw_networkx_edges(
            G, pos,
            edgelist=edge_list,
            edge_color=edge_color_vals,
            edge_cmap=plt.cm.Reds,
            arrows=True,
            arrowstyle='->',
            node_size=1500,
            width=2,
            ax=ax
        )
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_size=8, ax=ax, label_pos=0.5
        )
    else:
        nx.draw_networkx_edges(
            G, pos,
            edge_color="gray",
            arrows=True,
            arrowstyle='->',
            node_size=1500,
            ax=ax
        )

    if title:
        plt.title(title, fontsize=14)
    else:
        default_title = {
            "none": "BN Visualization (Simple)",
            "blanket": f"BN Visualization (Markov Blanket of '{target}')",
            "impacts": f"BN Visualization (Nodes Impact Over '{target}')",
            "edges": "BN Visualization (Edge Impacts)",
            "edges_and_impacts": f"BN Visualization (Edges Impact & Nodes Impact Over '{target}')"
        }
        plt.title(default_title.get(type, f"BN Visualization ({type})"), fontsize=14)

    plt.axis("off")

    if type == "blanket":
        legend_handles = [
            patches.Patch(color="lightgreen", label="Target"),
            patches.Patch(color="salmon", label="Markov Blanket"),
            patches.Patch(color="skyblue", label="Other Nodes")
        ]
        plt.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1.02, 0.5), frameon=True)

    plt.tight_layout()

    if filename:
        plt.savefig(filename, bbox_inches="tight", dpi=300)
        plt.close()
    else:
        with contextlib.redirect_stderr(sys.__stdout__):
            plt.show()