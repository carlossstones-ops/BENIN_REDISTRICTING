import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd
"""
# Step 1: Create a graph (simulating 10 counties)
G = nx.Graph()

# Add nodes (counties)
G.add_nodes_from(range(1, 11))  # counties 1 to 10

# Add edges (adjacency between counties)
edges = [
    (1, 2), (1, 3),
    (2, 4), (2, 5),
    (3, 5), (3, 6),
    (4, 7), (5, 7), (5, 8),
    (6, 8), (6, 9),
    (7, 10), (8, 10), (9, 10)
]
G.add_edges_from(edges)

# Step 2: Partition the graph manually (simulate redistricting)
# Assign each node to a district label (1, 2, or 3)
district_labels = {
    1: 1, 2: 1, 3: 1,
    4: 2, 5: 2, 6: 2,
    7: 3, 8: 3, 9: 3, 10: 3
}

# Step 3: Visualize the districts
pos = nx.spring_layout(G, seed=42)  # nice layout
colors = ['lightcoral', 'lightblue', 'lightgreen']

node_colors = [colors[district_labels[n]-1] for n in G.nodes]

plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=800, edge_color='gray')
plt.title("Toy Example of Redistricting (Graph Partitioning)")
plt.show()
"""

# Step 1 - Load Department-level GeoJson for BENIN

gdf=gpd.read_file(r"C:\Users\Carlos Stone\Documents\Visual Studio 2022\geoBoundaries-BEN-ADM3-all")

# print(gdf.head()) # How many rows (units) are in gdf

# Check if first two polygons touch

# print(gdf.geometry[0].touches(gdf.geometry[1])) #.touches() → returns True if two geometries share a border but do not overlap.




# Add an Identity column if none exists.

gdf['id'] = gdf.index

# Step 2 - Build adjacency graph

G=nx.Graph()

for idx, row in gdf.iterrows():
    G.add_node(row['id'], name=row['shapeName'])


# Add edges for polygons sharing borders

for i, poly in gdf.iterrows():
    
    for j, other in gdf.iterrows():
        
        if i < j and poly['geometry'].touches(other['geometry']):
            
            G.add_edge(poly['id'], other['id'])


#greedy_modularity_communities method finds clusters of nodes that have more edges inside the group than between groups plus it works without population data 

from networkx.algorithms import community

# Step 1: Detect communities (districts)
communities = community.greedy_modularity_communities(G)

# Step 2: Convert to district labels
district_labels = {}
for district_num, nodes in enumerate(communities, start=1):
    for node in nodes:
        district_labels[node] = district_num

# Step 3: Add labels to GeoDataFrame
gdf['district'] = gdf.index.map(district_labels)



plt.figure(figsize=(8, 12))
gdf.plot(column='district', categorical=True, cmap='Set2', legend=True)
plt.title("Benin - Algorithmically Generated Districts (Community Detection)", fontsize=14)
plt.axis('off')
plt.show()

"""""       
# Step 3: Assign labels (e.g. manually or algorithmically)

labels = {id_: (id_ % 3) + 1 for id_ in gdf['id']}

# Step 4: Plot map with district colors

district_colors = {1: 'red', 2: 'blue', 3: 'green'}

gdf['district'] = gdf['id'].map(labels)

gdf.plot(column='district', categorical=True, cmap='Set2', legend=True)

plt.title('Benin Simulated Districts (by Department)')

plt.axis('off')

plt.show()
"""""




