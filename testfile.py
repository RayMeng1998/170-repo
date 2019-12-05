import networkx as nx
def testfile():
    G = nx.Graph()
    G.add_nodes_from([1,2,3])
    G.add_weighted_edges_from([(1,2, 1), (1,3,1)])
    print(list(nx.dfs_preorder_nodes(G,1)))
    print(list(nx.dfs_postorder_nodes(G,1)))

testfile()
