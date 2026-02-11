import networkx as nx
import csv
from math import radians, cos, sin, asin, sqrt

# Specific to routes.csv file
def load_edges():
    routes = []
    with open("./data/archive/routes.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header
        for row in reader:
            src = row[3].strip()
            dst = row[5].strip()
            # routes.csv has \N for missing codes; skip those
            if src and dst and src != r"\N" and dst != r"\N":
                routes.append((src, dst))

    return routes

# Specific to Countries by continents.csv and airports.csv
def get_airport_attributes():
    country_and_continent = {}

    with open("./data/archive/Countries by continents.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header

        for row in reader:
            country = row[1].strip()
            if not country or country == r"\N":
                continue

            continent = row[0].strip()
            if not continent or continent == r"\N":
                continue

            country_and_continent[country] = {
                "continent": continent
            }

    # Countries with numerous airports not classified in Countries by continents.csv
    country_and_continent["Burma"] = {"continent": "Asia"}
    country_and_continent["Netherlands Antilles"] = {"continent": "North America"}
    country_and_continent["Czech Republic"] = {"continent": "Europe"}
    country_and_continent["Congo (Kinshasa)"] = {"continent": "Africa"}
    country_and_continent["Congo (Brazzaville)"] = {"continent": "Africa"}
    country_and_continent["Greenland"] = {"continent": "Europe"}
    country_and_continent["Cook Islands"] = {"continent": "Oceania"}
    country_and_continent["French Polynesia"] = {"continent": "Oceania"}
    country_and_continent["Puerto Rico"] = {"continent": "North America"}

    iata_to_attrs = {}

    with open("./data/archive/airports.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header

        for row in reader:
            iata = row[5].strip()
            if not iata or iata == r"\N":
                continue

            city = row[3].strip()
            if not city or city == r"\N":
                continue

            country = row[4].strip()
            if not country or country == r"\N":
                continue

            latitude = row[7].strip()
            if not latitude or latitude == r"\N":
                continue

            longitude = row[8].strip()
            if not longitude or longitude == r"\N":
                continue

            iata_to_attrs[iata] = {
                "city": city,
                "country": country,
                "continent": country_and_continent.get(country, {}).get("continent"),
                "latitude": float(latitude),
                "longitude": float(longitude)
            }

    return iata_to_attrs

def missing_info(G):
    nodes_to_remove = []

    # Iterate over all nodes along with their attribute dictionaries
    for node, attrs in G.nodes(data=True):

        # If a node has no attributes, remove it
        if not attrs or attrs["continent"] is None:
            nodes_to_remove.append(node)

    return nodes_to_remove

def compute_distances(G, routes):
    edge_distances = {}

    # Radius of Earth in km
    r = 6371

    for node1, node2 in routes:
        # From a known edge, get the latitude and longitude from each node the edge connects and convert to radians
        lat1, lon1 = radians(G.nodes[node1]["latitude"]), radians(G.nodes[node1]["longitude"])
        lat2, lon2 = radians(G.nodes[node2]["latitude"]), radians(G.nodes[node2]["longitude"])

        # Haversine formula
        diff_lon = lon2 - lon1
        diff_lat = lat2 - lat1
        a = sin(diff_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(diff_lon / 2) ** 2
        c = 2 * asin(sqrt(a))

        # Final distance
        d = r * c

        edge_distances[(node1, node2)] = d

    return edge_distances

def make_graph():
    # Generate graph via edge list of routes
    routes = load_edges()
    G = nx.Graph(routes)

    # Compile relevant airport information for node attributes
    attributes = get_airport_attributes()
    nx.set_node_attributes(G, attributes)

    # Disparities between CSV files
    to_remove = missing_info(G)
    G.remove_nodes_from(to_remove)

    # Isolate largest connected component
    largest_cc_nodes = max(nx.connected_components(G), key=len)
    G = G.subgraph(largest_cc_nodes).copy()
    G.remove_nodes_from(list(nx.isolates(G)))  # Just in case any isolated nodes are left

    # Add edge weights
    distances = compute_distances(G, list(G.edges()))
    nx.set_edge_attributes(G, distances, name="weight")

    return G