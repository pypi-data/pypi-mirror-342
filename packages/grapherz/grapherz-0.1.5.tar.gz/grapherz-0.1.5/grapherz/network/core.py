import networkx as nx
from networkx.drawing.nx_pydot import write_dot


class NetworkXGraph():
    def __init__(self):
        self.G = nx.Graph(day="Friday")
        # G.graph['day'] = "Monday"

        nx.DiGraph(G)
        G = nx.Graph()
        
        
    def add_node(self, key,by:str):
        if by == 'list':
            self.G.add_nodes_from(key, time='5pm')
        elif by == 'cell':
            self.G.add_node(key, time='2pm')
        
    def add_edge(self, key, by:str): # G.add_edge(1, 2)
        if by == 'list':
            self.G.add_edges_from(key)
        elif by == 'cell':
            self.G.add_edge(key)
            
    def get_number(self, type = 'nodes'):
        if type == 'nodes':
            return G.number_of_nodes()
        elif type == 'edges':
            return G.number_of_edges()
        
    def remove_node(self, key, by:str):
        if by == 'list':
            self.
#             G.remove_edge(1, 3) G.remove_node(2)
    
    def clear(self):
        self.G.clear()
       
    def draw(self):
        nx.draw(self.G, with_labels=True, font_weight='bold')
        
    def get_node(self):
        G.nodes[1]
        
        
    def work(self):
        assert list(DG.successors(2)) == [1, 4]
        assert list(DG.edges) == [(2, 1), (2, 4), (1, 3), (1, 2)]