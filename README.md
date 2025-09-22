# Quantum Walk Simulation & Visualisation

This repository contains Python code for studying **discrete-time quantum walks on graphs**.  
A quantum walk is the quantum analogue of a classical random walk. While a classical random walk’s variance grows linearly with the number of steps, a quantum walk spreads quadratically faster and exhibits interference effects.

The project provides:
- Quantum walk circuit construction and simulation.
- Graph generation and adjacency matrix utilities.
- Visualisation tools for probability distributions and walks.

---

## Project structure

```
.
├── pyproject.toml              # Build system + dependencies
├── requirements.txt            # Python dependencies
├── LICENSE                     # Apache 2.0 license
├── README.md                   # This file
├── src/
│   └── qwalk/
│       ├── __init__.py
│       ├── circuit.py          # QuantumWalkCircuit: build/simulate circuits
│       ├── graph.py            # WalkGraph: graph generation + adjacency matrices
│       └── visuals.py          # QuantumWalkVisuals: plotting + probability viz
└── tests/
    ├── test_circuit.py
    ├── test_graph.py
    └── test_visuals.py
```

---

## Modules

### `circuit.py`
Implements **discrete-time quantum walks** on arbitrary graphs:
- Encodes walker position in a register of qubits.
- Uses one or more qubits as the “coin” to decide movement direction.
- Iterates coin + shift operators based on the adjacency matrix.
- Runs on simulators (Qiskit Aer) or real backends (IBM Quantum).

### `graph.py`
- Utilities to build standard graphs (lines, cycles, hypercubes, etc.).
- Provides adjacency, degree, and Laplacian matrices.
- Ensures stable node ordering for consistent mapping.

### `visuals.py`
- Plot graphs with Matplotlib + NetworkX.
- Show probability distributions of the walker.
- Animate the evolution of the walk.
- Colour nodes based on measured probabilities.

---

## Installation

Clone and install in editable mode:

```bash
git clone https://github.com/yourusername/qwalk.git
cd qwalk
pip install -e ".[viz]"
```

Dependencies include:
- `numpy`, `scipy`, `networkx`, `matplotlib`
- `qiskit` (for quantum circuit simulation)

---

## Usage

### 1. Build a graph
```python
from qwalk.graph import WalkGraph

wg = WalkGraph.from_cycle(8)
A = wg.adjacency_matrix()
```

### 2. Simulate a quantum walk
```python
from qwalk.circuit import QuantumWalkCircuit

qc = QuantumWalkCircuit(wg.graph, num_steps=5).build()
```

### 3. Visualise results
```python
from qwalk.visuals import QuantumWalkVisuals

vis = QuantumWalkVisuals(results, counts, wg)
vis.coloured_graph(savepath="qwalk.png")
```

---

## Tests

Run the test suite with:

```bash
pytest
```

- `test_circuit.py` checks circuit construction.  
- `test_graph.py` validates graph utilities and adjacency/Laplacian matrices.  
- `test_visuals.py` ensures plots and visualisations generate correctly.

---

## Citations

This project draws on several key resources:

1. Cirq educational material on **quantum vs classical random walks**.  
2. NetworkX documentation for `adjacency_matrix(G)`.  
3. D. Aharonov, A. Ambainis, J. Kempe, and U. Vazirani,  
   *Quantum Walks on Graphs*, STOC ’01, arXiv:quant-ph/0012090.

---

## License

This project is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).  
See the `LICENSE` file for details.

---
