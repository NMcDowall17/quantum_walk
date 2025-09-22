import os
import numpy as np
import networkx as nx
import pytest

from qwalk.graph import WalkGraph
@pytest.fixture
def line5():
    return walk_graph.from_line(5)

@pytest.fixture
def cycle4():
    return walk_graph.from_cycle(4)

@pytest.fixture
def hypercube3():
    return walk_graph.from_hypercube(3)


def test_rejects_non_graph():
    with pytest.raises(ValueError):
        walk_graph(graph=123)

def test_rejects_empty_graph():
    G = nx.Graph()
    with pytest.raises(ValueError):
        walk_graph(G)

def test_stable_order_sorted(line5):
    assert line5.nodes == sorted(line5.graph.nodes())
    assert line5.length == len(line5.nodes)
    assert all(line5.index[node] == i for i, node in enumerate(line5.nodes))

def test_custom_order_is_respected():
    G = nx.path_graph(4)
    custom = [2, 0, 3, 1]
    wg = walk_graph(G, ordering=custom)
    assert wg.nodes == custom
    assert wg.index[2] == 0 and wg.index[1] == 3

def test_from_line_and_cycle(line5, cycle4):
    assert line5.length == 5
    assert cycle4.length == 4
    A_line = line5.adjacency_matrix()
    A_cycle = cycle4.adjacency_matrix()
    assert A_line.shape == (5, 5)
    assert A_cycle.shape == (4, 4)

def test_from_hypercube_relabels_to_bitstrings(hypercube3):
    assert all(isinstance(n, str) and set(n) <= {"0", "1"} for n in hypercube3.nodes)
    assert len(hypercube3.nodes) == 8
    assert hypercube3.nodes == sorted(hypercube3.nodes)

def test_from_hypercube_without_relabel():
    wg = walk_graph.from_hypercube(2, relabel_to_bitstrings=False)
    assert all(isinstance(n, tuple) for n in wg.nodes)
    assert len(wg.nodes) == 4

def test_adjacency_respects_node_order(line5):
    A = line5.adjacency_matrix().toarray()
    assert A.shape == (5, 5)
    assert np.all(A == A.T)
    degs = A.sum(axis=1)
    assert list(degs) == [1, 2, 2, 2, 1]

def test_degree_matrix_exists_and_diagonal(line5):
    D = line5.degree_matrix()
    if hasattr(D, "toarray"):
        D = D.toarray()
    assert D.shape == (5, 5)
    assert np.allclose(D, np.diag([1, 2, 2, 2, 1]))

def test_laplacian_matrix_unormalized(line5):
    L = line5.laplacian_matrix(normalized=False)
    if hasattr(L, "toarray"):
        L = L.toarray()
    A = line5.adjacency_matrix().toarray()
    D = np.diag([1, 2, 2, 2, 1])
    assert np.allclose(L, D - A)

def test_laplacian_matrix_normalized(cycle4):
    Ln = cycle4.laplacian_matrix(normalized=True)
    if hasattr(Ln, "toarray"):
        Ln = Ln.toarray()
    assert np.allclose(Ln, Ln.T)
    w = np.linalg.eigvalsh(Ln)
    assert np.isclose(w.min(), 0.0, atol=1e-9)

def test_plt_visualize_creates_file(tmp_path, line5):
    savepath = tmp_path / "walk_graph.png"
    out = line5.plt_visualize(figsize=(3, 3), savepath=savepath)
    assert os.path.exists(out)
    assert str(out).endswith(".png")

def test_stable_order_custom_list_is_idempotent(line5):
    custom = [4, 3, 2, 1, 0]
    assert walk_graph(line5.graph, ordering=custom).nodes == custom
