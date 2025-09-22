import os
import numpy as np
import networkx as nx
import pytest
from qiskit import QuantumCircuit
import networkx as nx 
import matplotlib.pyplot as plt 
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.exceptions import IBMRuntimeError, IBMInputValueError
from qiskit.circuit.library import CDKMRippleCarryAdder
import math 
from qiskit_aer import AerSimulator
from qiskit import transpile 
import numpy as np 
import pandas as pd 
from qiskit.result import Result    
from Quantum_walk_circuit import Quantum_walk_circuit
from Walk_graph import walk_graph
import matplotlib.cm as cm

class Quantum_walk_visuals: 
    # graph in these parameters is a walk_graph obj instead of nx.graph, bc it lets you get the index + 
    # stable node ordering 
    def __init__(self,results: Result, counts: dict[str, int], graph:walk_graph):  
        self.counts = counts
        self.results = results 
        if not isinstance(graph, walk_graph): 
             raise ValueError("graph must be walk_graph obj")
        self.graph = graph.graph 
        self.index = graph.index
        self.nodes = graph.nodes
        total =  sum(counts.values()) 
        self.total = total
        # probablity per node
        PPN = {}
        for i in counts: 
            Prob = counts[i]/total 
            PPN[i] = Prob 
        self.PPN = PPN  
        self.labels = {node: f"p={self.PPN.get(node, 0.0):.2f}" for node in self.nodes} 
    def Quantum_walk_histogram(self, figsize: (int,int)): 
        x_data = list(self.counts.keys()) 
        y_data_shots = [self.counts[i] for i in x_data ]
        y_data_probs = [self.PPN[i] for i in x_data] 

    #shows histogram of bitstring versus shots 
        plt.figure(figsize=figsize) 
        plt.bar(x_data, y_data_shots, color="skyblue")
        plt.xlabel("Bitstring outcome")
        plt.ylabel("Counts")
        plt.title("Histogram of measurement outcomes")
        plt.xticks(rotation=45)   # so bitstrings don’t overlap
        plt.tight_layout()
        plt.show() 
    #shows histogram of bitstring versus probs 
        plt.figure(figsize=figsize) 
        plt.bar(x_data, y_data_probs, color="skyblue")
        plt.xlabel("Bitstring outcome")
        plt.ylabel("Counts")
        plt.title("Histogram of measurement outcomes")
        plt.xticks(rotation=45)   # so bitstrings don’t overlap
        plt.tight_layout()
        plt.show() 
    def coloured_graph(self, savepath= False): 
        cmap = cm.get_cmap("viridis") 
        colored_nodes = [cmap(self.PPN.get(node, 0)) for node in self.nodes] 
        nx.draw(G=self.graph, labels=self.labels,nodelist=self.nodes, node_color=colored_nodes) 
        if savepath is not False: 
            plt.show()
            savepath = save_path= f"Quantum_walk_graph_colored{time.strftime("%Y%m%d-%H%M%S")}.png" 
            plt.savefig(savepath, bbox_inches="tight")
            plt.close()
            return savepath
        else:
            plt.show()
            plt.close()


    







