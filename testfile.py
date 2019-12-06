import networkx as nx
from utils import *
from student_utils import *
def testfile():
    G = nx.Graph()
    G.add_nodes_from([1,2,3])
    G.add_weighted_edges_from([(1,2, 1), (1,3,1)])
    print(list(nx.shortest_path(G, 1, 2)))


testfile()
