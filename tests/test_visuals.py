import networkx as nx
import numpy as np
import pytest

from Walk_graph import walk_graph
from Quantum_walk_visuals import Quantum_walk_visuals  # adjust import if needed

class DummyResult:  # minimal placeholder; we only test visuals logic here
    pass

def test_visuals_init_builds_ppn_and_labels():
    # Make a tiny graph with stable bitstring labels
    wg = walk_graph.from_hypercube(2)  # nodes: '00','01','10','11' (sorted by your class)

    # Counts that sum to 100
    counts = {'00': 50, '01': 25, '10': 25}  # '11' missing -> prob should default to 0.0 in labels

    vis = Quantum_walk_visuals(DummyResult(), counts, wg)

    # Probabilities expected
    assert vis.total == 100
    assert np.isclose(vis.PPN['00'], 0.5)
    assert np.isclose(vis.PPN['01'], 0.25)
    assert np.isclose(vis.PPN['10'], 0.25)

    # Missing key handled (get(..., 0.0))
    assert vis.PPN.get('11', 0.0) == 0.0

    # Labels use two decimal places
    assert vis.labels['00'] == "p=0.50"
    assert vis.labels['01'] == "p=0.25"
    assert vis.labels['10'] == "p=0.25"
    assert vis.labels['11'] == "p=0.00"
