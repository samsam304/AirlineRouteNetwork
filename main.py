from DataScraper import *
from GraphMetrics import *
from GraphVisualizations import *
from Subgraph import *
from Communities import *

def continent_clustering(G):
    # Create subgraph and add nodes as names of continents
    continents = ["Asia", "North America", "South America", "Europe", "Africa", "Oceania"]
    C = generate_clusters_by_node_list(G, continents, "continent")

    # Add population densities to each continent
    pop_attrs = {'Asia': {'population': 4581757408},
                 'Europe': {'population': 738849000},
                 'Africa': {'population': 1216130000},
                 'North America': {'population': 579024000},
                 'South America': {'population': 422535000},
                 'Oceania': {'population': 38304000}
                 }

    nx.set_node_attributes(C, pop_attrs)

    # Uncomment for visualization
    display_spring_layout_edge_labes(C)

    return C

# Takes forever
def country_clustering(G):
    # Create subgraph and add nodes as names of countries
    countries = set()
    for node in G.nodes():
        country = G.nodes[node]['country']
        countries.add(country)

    print(len(countries))

    C = generate_clusters_by_node_list(G, countries, 'country')

    return C

def continent_flight_analysis_bar_chart(G):
    labels = ["Asia", "North America", "South America", "Europe", "Africa", "Oceania"]
    intra_flights = []
    for continent in labels:
        intra_flights.append(edges_within(G, continent, "continent"))

    inter_flights = []
    for continent in labels:
        total = 0
        for y in labels:
            if continent != y:
                total += edges_between(G, continent, y, "continent")
        inter_flights.append(total)

    grouped_bar_chart(G, labels, intra_flights, inter_flights,
                      'Intracontinental Flights', 'Intercontinental Flights',
                      'Continents', 'Number of Flights', 'Continental Flight Analysis')

def main():
    # Construct the global graph with all attributes
    G = make_graph()

    airport = "SVO"
    print(f"{G.nodes[airport]["country"]} is in: {G.nodes[airport]['continent']}")

if __name__ == "__main__":
    main()
