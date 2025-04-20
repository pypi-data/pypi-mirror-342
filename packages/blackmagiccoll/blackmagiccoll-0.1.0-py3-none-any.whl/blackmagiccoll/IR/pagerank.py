import networkx as nx

webgraph = nx.DiGraph()
webgraph.add_edges_from([
    ('A','B'),
    ('A','C'),
    ('A','D'),
    ('B','C'),
    ('B','E'),
    ('C','A'),
    ('C','D'),
])

pagerank_scores = nx.pagerank(webgraph,alpha=0.85)

for node , score in pagerank_scores.items():
  print(f"PageRank Score for {node}: {score}")

sorted_nodes = sorted(pagerank_scores,key=pagerank_scores.get,reverse=True)
print("Sorted Nodes:")
for node in sorted_nodes:
  print(f"{node}: {pagerank_scores[node]:.4f}")