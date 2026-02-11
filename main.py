import networkx as nx
import csv
from networkx.classes import subgraph, get_edge_attributes, degree_histogram
import networkx.classes.function as fn
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations

from networkx.drawing import planar_layout
from scipy.cluster.hierarchy import weighted

from DataScraper import *
from GraphMetrics import *
from GraphVisualizations import *
from Subgraph import *
from Communities import *

def continent_clustering(G):
    # Create subgraph and add nodes as names of continents
    continents = ["Asia", "North America", "South America", "Europe", "Africa", "Oceania"]
    C = generate_clusters_by_node_list(G, continents)

    # Add population densities to each continent
    pop_attrs = {'Asia': {'population': 4581757408},
                 'Europe': {'population': 738849000},
                 'Africa': {'population': 1216130000},
                 'North America': {'population': 579024000},
                 'South America': {'population': 422535000},
                 'Oceania': {'population': 38304000}
                 }

    nx.set_node_attributes(C, pop_attrs)

    # display_spring_layout_edge_labes(C)

    return C

def continent_flight_analysis_bar_chart(G):
    labels = ["Asia", "North America", "South America", "Europe", "Africa", "Oceania"]
    intra_flights = []
    for continent in labels:
        intra_flights.append(edges_within(G, continent))

    inter_flights = []
    for continent in labels:
        total = 0
        for y in labels:
            if continent != y:
                total += edges_between(G, continent, y)
        inter_flights.append(total)

    grouped_bar_chart(G, labels, intra_flights, inter_flights,
                      'Intracontinental Flights', 'Intercontinental Flights',
                      'Continents', 'Number of Flights', 'Continental Flight Analysis')

def main():
    # Construct the global graph with all attributes
    G = make_graph()

    assign_greedy_communities(G, "weight", 15)

    draw_world_map_by_community(G)

if __name__ == "__main__":
    main()
