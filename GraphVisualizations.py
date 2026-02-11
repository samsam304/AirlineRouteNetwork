import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

def draw_world_map(G):
    plt.figure(figsize=(14, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())

    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAND, edgecolor="black", linewidth=0.2)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.4)
    ax.add_feature(cfeature.BORDERS, linewidth=0.2)

    gl = ax.gridlines(draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False

    # edges
    for node1, node2 in G.edges():
        lat1, lon1 = G.nodes[node1]["latitude"], G.nodes[node1]["longitude"]
        lat2, lon2 = G.nodes[node2]["latitude"], G.nodes[node2]["longitude"]
        ax.plot(
            [lon1, lon2],
            [lat1, lat2],
            transform=ccrs.PlateCarree(),
            linewidth=0.2,
            alpha=0.15
        )

    # nodes
    lons = [G.nodes[n]["longitude"] for n in G.nodes()]
    lats = [G.nodes[n]["latitude"] for n in G.nodes()]
    ax.scatter(lons, lats, transform=ccrs.PlateCarree(), s=3, color="red")

    plt.title("Air Route Network")
    plt.show()

def degree_distribution_hist(degrees, graph_name):
    degree_counts = np.array(degrees)
    degree_hist = np.arange(1, len(degree_counts) + 1)

    plt.figure(figsize=(10, 6))
    plt.bar(degree_hist, degree_counts, width=1.0, edgecolor="black")

    plt.xlabel("Degree")
    plt.ylabel("Number of Airports")
    plt.title(f"Degree Distribution of the {graph_name} Airline Route Network")

    plt.show()

def degree_distribution_scatter(degrees, graph_name):
    degree_counts = np.array(degrees)
    degree_hist = np.arange(1, len(degree_counts) + 1)
    mask = degree_counts > 0

    plt.figure(figsize=(10, 6))
    plt.scatter(degree_hist[mask], degree_counts[mask], s=15)

    plt.xscale("log")
    plt.yscale("log")

    plt.xlabel("Degree")
    plt.ylabel("Number of Airports")
    plt.title(f"Log-Log Degree Distribution of the {graph_name} Airline Route Network")

    plt.show()

def display_spring_layout_edge_labes(G):
    pos = nx.spring_layout(G, weight='inv_weight', seed=23, k=1.2, iterations=100)
    nx.draw(G, pos, with_labels=True, node_size=2500, node_color='lightblue', font_weight='bold', font_size=10)
    nx.draw_networkx_edge_labels(G, pos, label_pos=0.6, edge_labels=nx.get_edge_attributes(G, "weight"), font_weight='bold')
    plt.show()

def grouped_bar_chart(G, labels ,data1, data2, data1_label, data2_label, xlabel, ylabel, title):
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x - width / 2, data1, width, label=data1_label)
    ax.bar(x + width / 2, data2, width, label=data2_label)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x, labels)
    ax.legend()

    fig.tight_layout()

    plt.show()