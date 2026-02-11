import networkx as nx
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def assign_greedy_communities(G, weight, best_n, community_attr="community",return_sets=False):
    communities = list(nx.community.greedy_modularity_communities(G, weight=weight, best_n=best_n))

    node_to_comm = {}
    for comm_id, nodeset in enumerate(communities):
        for n in nodeset:
            node_to_comm[n] = comm_id
            G.nodes[n][community_attr] = comm_id

    if return_sets:
        return node_to_comm, communities
    return node_to_comm

def draw_world_map_by_community(G, community_attr="community", show_legend=True):
    # Collect nodes with valid lat/lon + community
    nodes = []
    lats = []
    lons = []
    comms = []

    for n, d in G.nodes(data=True):
        if community_attr not in d:
            continue
        nodes.append(n)
        lats.append(d["latitude"])
        lons.append(d["longitude"])
        comms.append(d[community_attr])

    if not nodes:
        raise ValueError(
            f"No drawable nodes found. Ensure nodes have latitude/longitude and '{community_attr}'."
        )

    unique_comms = sorted(set(comms))
    n_comms = len(unique_comms)

    # Build a stable community -> color index mapping
    comm_to_idx = {c: i for i, c in enumerate(unique_comms)}

    # Use a qualitative colormap (cycles if > N colors)
    cmap = plt.cm.get_cmap("tab20", max(n_comms, 1))

    plt.figure(figsize=(14, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAND, edgecolor="black", linewidth=0.2)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.4)
    ax.add_feature(cfeature.BORDERS, linewidth=0.2)

    gl = ax.gridlines(draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False

    # Draw nodes by community (one scatter per community for clean legend + consistent colors)
    handles = []
    labels = []

    for c in unique_comms:
        idx = comm_to_idx[c]
        color = cmap(idx % cmap.N)

        comm_lons = [lon for lon, cc in zip(lons, comms) if cc == c]
        comm_lats = [lat for lat, cc in zip(lats, comms) if cc == c]

        sc = ax.scatter(
            comm_lons,
            comm_lats,
            transform=ccrs.PlateCarree(),
            s=8,
            color=color,
            alpha=0.9,
            linewidths=0,
        )

        handles.append(sc)
        labels.append(f"Community {c+1} ({len(comm_lons)})")

    if show_legend and n_comms <= 25:
        ax.legend(handles, labels, loc="lower left", fontsize=8, frameon=True)

    plt.title(f"Air Route Network (nodes colored by {community_attr})")
    plt.show()