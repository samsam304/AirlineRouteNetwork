import networkx as nx
from networkx.classes import subgraph
from itertools import combinations
from GraphMetrics import *

def subgraph_by_continent(G, continent):
    airports = list(G.nodes())
    sub_airports = []

    for airport in airports:
        if G.nodes[airport]["continent"] == continent:
            sub_airports.append(airport)

    sub_G = subgraph(G, sub_airports)

    largest_cc_nodes = max(nx.connected_components(sub_G), key=len)
    sub_G = sub_G.subgraph(largest_cc_nodes).copy()

    sub_G.remove_nodes_from(list(nx.isolates(sub_G)))

    return sub_G

def generate_clusters_by_node_list(G, node_list):
    C = nx.Graph()
    C.add_nodes_from(node_list)

    # Generate all possible edges between nodes (not optimal for general case)
    combos = list(combinations(node_list, 2))

    # Store number of airports in each continent
    for node in node_list:
        count = nodes_per_continent_val(G, node)
        C.nodes[node]["airports"] = count

    # Edges Between
    for c1, c2 in combos:
        edges = edges_between(G, c1, c2)
        if edges > 0:
            C.add_edge(c1, c2, weight=edges)

    return C