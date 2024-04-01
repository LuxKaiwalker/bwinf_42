import networkx as nx
import matplotlib.pyplot as plt
from adjustText import adjust_text

def display_graph_with_values(graph):
    G = nx.Graph()

    for node, (adj_nodes, values) in graph.items():
        G.add_node(node, label=f"{node}\n{values}")

        for adj_node in adj_nodes:
            G.add_edge(node, adj_node)

    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')

    nx.draw(G, pos, with_labels=False, node_size=800, node_color='skyblue', font_size=8)

    # Draw node labels with adjusted positions to prevent overlap
    text_objects = [plt.text(pos[node][0], pos[node][1], labels[node], fontsize=8, ha='center', va='center') for node in G.nodes]
    adjust_text(text_objects, arrowprops=dict(arrowstyle="-", color='black', lw=0.5))

    plt.show()

# Example usage:
my_graph = {
    1: [[2, 3], [4, 5]],
    2: [[1, 3], [6, 7]],
    3: [[1, 2], [8, 9]],
}

display_graph_with_values(my_graph)
