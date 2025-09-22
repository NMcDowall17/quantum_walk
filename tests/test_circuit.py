import networkx as nx
from qiskit import QuantumCircuit
import pytest

from qwalk.circuit import QuantumWalkCircuit


def test_build_compiles():
    G = nx.path_graph(3)
    obj = Quantum_walk_circuit(G, num_steps=1)
    qc = obj.build()
    assert isinstance(qc, QuantumCircuit)
    assert qc.num_qubits >= obj.q_pos * 2 + obj.q_coin

def test_coin_h_count():
    G = nx.path_graph(4)
    obj = Quantum_walk_circuit(G, num_steps=1)
    qc = obj.build()
    h_on_coin = sum(1 for inst, _, _ in qc.data if inst.name == "h")
    assert h_on_coin >= obj.q_coin