import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import time 
import networkx as nx 
from pathlib import Path 


class walk_graph: 
    def __init__(self, graph: nx.Graph,ordering="auto"): 
        if not isinstance(graph, nx.Graph): 
            raise(ValueError("obj. must be a nx.Graph")) 
        if graph.number_of_nodes() == 0: 
            raise(ValueError("empty graph was passed"))
        self.graph = graph.copy() 
        self.nodes = self.stable_order(ordering) 
        self.length = len(self.nodes) 
        self.index = {node:i for i, node in enumerate(self.nodes)}  
    @classmethod
    def from_hypercube(cls, n: int, relabel_to_bitstrings: bool = True, **kw):
        if not isinstance(n, int) or n < 1: 
            raise(ValueError("none integer and positive n passed"))
        G = nx.hypercube_graph(n)
        if relabel_to_bitstrings:
            mapping = {u: ''.join(map(str, u)) for u in G.nodes()}
            G = nx.relabel_nodes(G, mapping)
        return cls(G, **kw) 
    @classmethod
    def from_line(cls, n: int, **kw):
        return cls(nx.path_graph(n), **kw)

    @classmethod
    def from_cycle(cls, n: int, **kw):
        return cls(nx.cycle_graph(n), **kw)   
    def plt_visualize(self, figsize: (12,12), savepath= False):  
        cords = nx.spring_layout(self.graph, seed= 7)
        plt.figure(figsize=figsize)
        nx.draw(self.graph, cords, with_labels=True, node_size=600)
        plt.tight_layout()
        if savepath is not False:
            save_path= f"Quantum_walk_graph{time.strftime("%Y%m%d-%H%M%S")}.png"
            plt.savefig(savepath, bbox_inches="tight")
            return savepath
        else:
            plt.show()
            plt.close()
    def stable_order(self, ordering, *kwargs):
        if ordering == "auto":
            return sorted(self.graph.nodes())
        else:
            return ordering 
   
    def adjacency_matrix(self, *kwargs):
        return nx.adjacency_matrix(self.graph, nodelist=self.nodes)
    
    def degree_matrix(self, **_, ):
        degs = [d for _, d in self.graph.degree(self.nodes)]
        return np.diag(degs)
    
    def laplacian_matrix(self, normalized: bool = False, **_):
        if normalized:
            return nx.normalized_laplacian_matrix(self.graph, nodelist=self.nodes)
        return nx.laplacian_matrix(self.graph, nodelist=self.nodes)
      
        
    

  