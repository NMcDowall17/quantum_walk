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

class Quantum_walk_circuit: 
    def __init__(self,graph:nx.Graph, num_steps:int): 
        if not isinstance(graph, nx.Graph):  
            raise(ValueError("Graph obj is not nx.Graph"))
        G = graph.copy() 
        deg = dict(G.degree()) 
        self.degs = deg
        self.graph = G 
        q_pos = max(1, math.ceil(math.log2(G.number_of_nodes()))) 
        if not isinstance(q_pos, int) or q_pos < 1: 
            raise(ValueError("q_pos must be int and >1"))
        self.q_pos = q_pos
        self.max_deg = max(self.degs.values(), default=0) 
        self.q_coin = max(1, math.ceil(math.log2(max(1, self.max_deg))))
        self.num_steps = num_steps  
        if not isinstance(num_steps, int) or num_steps < 1: 
            raise(ValueError("Num_steps must be int and >1")) 
    
    def build(self): 
        q_pos = QuantumRegister(self.q_pos, "pos") 
        q_one = QuantumRegister(self.q_pos, "q_one")  
        q_coin = QuantumRegister(self.q_coin, "q_coin") 
        regs = [q_pos, q_one,q_coin]
        
        Base_adder = CDKMRippleCarryAdder(num_state_qubits= self.q_pos, kind="fixed").to_gate(label="adder")
        control = Base_adder.control(num_ctrl_qubits= self.q_coin) 
        
        anc_slice = []
       
       #identify how many ancillia qubits you need
        needed = Base_adder.num_qubits            # total qubits the adder expects
        have   = len(q_pos) + len(q_one)             # pos + one
        
        anc_needed = max(0, needed - have)
        if anc_needed > 0:
            anc = QuantumRegister(anc_needed, "anc")
            anc_slice = list(anc)
            regs.append(anc)
        qc = QuantumCircuit(*regs) 

        #nested loop applies the shift  of the H gates your applying
        for _ in range(self.num_steps):           # outer loop = steps
            for i in range(self.q_coin):          # inner loop = over coin qubits
                qc.h(q_coin[i])                   # apply H to coin[i]
        for i in q_pos: 
            qc.x(i) 
            # if coin is 1 then +1
            qc.append(control, [q_coin[0], *q_pos, *q_one, *anc_slice])
            
            # if coin is zero then -1
            qc.x(q_coin[0])
            qc.append(control.inverse(), [q_coin[0], *q_pos, *q_one, *anc_slice])
            qc.x(q_coin[0]) 
        self.qc =qc 
        return qc
    def run(self,device_name:str, real:bool=False,): 
        qc = self.qc
        if real == False: 
            backend = AerSimulator() 
            tcirc = transpile(qc, backend)               # qc = your QuantumCircuit
            job = backend.run(tcirc, shots=2000)
            result = job.result()
            counts = result.get_counts(tcirc) 
        if real == True:  
            if device is None: 
                raise ValueError("if not sim a device is needed")
            try: 
                service = QiskitRuntimeService()   # will raise if no saved account / misconfig
            except QiskitRuntimeServiceError as err:
                raise RuntimeError("Could not initialize QiskitRuntimeService. ","Make sure you have saved your IBM Quantum account with `QiskitRuntimeService.save_account(...)`.") from err
            backend = service.backend(device_name)       # pick a real device you have access to
            tcirc = transpile(qc, backend)
            job = backend.run(tcirc, shots=2000)      
            result = job.result()
            counts = result.get_counts(tcirc) 
        return results, counts 


        
        
        
        
