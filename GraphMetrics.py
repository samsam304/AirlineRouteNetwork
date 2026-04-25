import networkx as nx
from networkx.algorithms import cluster
import networkx.classes.function as fn

def get_stats(G):
    # Number of Nodes
    print(f"Number of nodes: {G.number_of_nodes()}")

    # Number of Edges
    print(f"Number of edges: {G.number_of_edges()}")

    # Average Degree
    avg_degree = (2 * G.number_of_edges()) / G.number_of_nodes()
    print(f"Average Network Degree: {avg_degree:.2f}")

    # Clustering Coefficient
    clust_coeff = cluster.average_clustering(G)
    print(f"Average Clustering Coefficient: {clust_coeff:.2f}")

    # Average Shortest Path (weighted or unweighted)
    from networkx.algorithms import shortest_paths
    short_path = shortest_paths.average_shortest_path_length(G)
    print(f"Average Shortest Path Length: {short_path:.2f}")

def single_degree_distribution(G, k):
    degrees = fn.degree_histogram(G)
    degree_k = degrees[k]
    degree_dist = degree_k / G.number_of_nodes()

    print(f"Distribution of Degree {k}: {degree_dist:.2f}")

def max_degree(G):
    degrees = fn.degree_histogram(G)
    print(f"Max Degree: {len(degrees)-1}")

def nodes_w_degree(G, k):
    node_w_degree = [node for node, degree in G.degree() if degree == k]

    print(f"Airports with degree {k}: {node_w_degree}")

def nodes_per_attribute(G, attribute, attribute_name):
    continents = nx.get_node_attributes(G, attribute_name)

    count = 0
    for airport in continents.values():
        if airport == attribute:
            count += 1

    print(f"Number of Airports in {attribute}: {count}")

def nodes_per_attribute_val(G, attribute, attribute_name):
    continents = nx.get_node_attributes(G, attribute_name)

    count = 0
    for airport in continents.values():
        if airport == attribute:
            count += 1

    return count

def edges_between(G, con1, con2, attribute):
    count = 0
    for node1, node2 in G.edges():
        c1 = G.nodes[node1][attribute]
        c2 = G.nodes[node2][attribute]
        if (c1 == con1 and c2 == con2) or (c1 == con2 and c2 == con1):
            count += 1

    return count

def edges_within(G, con, attribute):
    count = 0
    for node1, node2 in G.edges():
        c1 = G.nodes[node1][attribute]
        c2 = G.nodes[node2][attribute]
        if c1 == con and c2 == con:
            count += 1

    return count


