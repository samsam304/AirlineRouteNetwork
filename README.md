# AirlineRouteNetwork

Graph-theoretic analysis of the global airline route network using [NetworkX](https://networkx.org/). The world's airports become nodes, direct flight routes become edges, and Haversine great-circle distances become edge weights — letting us compute centrality, communities, degree distributions, intercontinental connectivity, and visualize the whole thing on a world map.

## Data

Source CSVs live in `data/archive/` (originally from the [OpenFlights](https://openflights.org/data.html) dataset plus a couple of supplementary files):

| File | Used for |
| --- | --- |
| `routes.csv` | Edge list — source/destination IATA pairs |
| `airports.csv` | Node attributes — city, country, latitude, longitude |
| `Countries by continents.csv` | Country → continent mapping |
| `country_population.csv` | Country populations (used in `country_clustering.ipynb`) |
| `airlines.csv`, `airplanes.csv` | Reserved for future analyses |

## Project layout

```
.
├── DataScraper.py            # Load CSVs, build the graph, compute Haversine edge weights
├── GraphMetrics.py           # Stats: degree, clustering, shortest paths, edges within/between groups
├── GraphVisualizations.py    # World-map plot, degree distributions, spring layouts, bar charts
├── Subgraph.py               # Continent subgraphs and attribute-based cluster graphs
├── Communities.py            # Greedy-modularity community detection + community-colored world map
├── main.py                   # Entry point — runs continent/country clustering and flight analysis
├── nx_basics.ipynb           # NetworkX intro / scratch
├── nx_algorithms.ipynb       # Algorithm exploration
├── graph_generation.ipynb    # Walk-through of building G from the CSVs
├── country_clustering.ipynb  # Country-level cluster graph + analyses
└── data/archive/             # Source CSVs
```

### Module overview

- **`DataScraper.make_graph()`** — the canonical way to build the working graph. Loads routes, attaches airport attributes (city/country/continent/lat/lon), drops nodes missing a continent, isolates the largest connected component, and assigns Haversine distance as edge `weight`.
- **`GraphMetrics`** — helpers like `get_stats(G)`, `nodes_per_attribute`, `edges_within(G, group, attr)`, and `edges_between(G, a, b, attr)` for slicing the network by continent or country.
- **`Subgraph.subgraph_by_continent(G, "Asia")`** and **`generate_clusters_by_node_list(G, nodes, attr)`** — pull regional subgraphs or collapse the network into a cluster-of-clusters graph (e.g. one node per continent, edge weights = number of flights between them).
- **`Communities.assign_greedy_communities(G, weight, best_n)`** — runs `nx.community.greedy_modularity_communities` and tags each node with a community id; `draw_world_map_by_community` plots the result.
- **`GraphVisualizations`** — `draw_world_map(G)`, `degree_distribution_hist`, `degree_distribution_scatter` (log-log), `display_spring_layout_edge_labes`, and `grouped_bar_chart`.

## Setup

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install networkx matplotlib numpy cartopy jupyter
```

> `cartopy` is the trickiest dep — on macOS it usually installs cleanly via `pip`; on Linux you may need `proj` and `geos` system packages first.

## Running

```bash
python main.py
```

Or open any of the notebooks:

```bash
jupyter lab
```

`graph_generation.ipynb` is a good place to start — it walks through how `DataScraper.make_graph()` constructs the graph step by step.

## Quick example

```python
from DataScraper import make_graph
from GraphMetrics import get_stats
from GraphVisualizations import draw_world_map

G = make_graph()
get_stats(G)
draw_world_map(G)
```
