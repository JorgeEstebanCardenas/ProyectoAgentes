import networkx as nx

# Pandas
import pandas as pd

import numpy as np

# Mostrar imágenes
from IPython.display import HTML

# Mathplotlib
import matplotlib.pyplot as plt

def crearRutas(start,end):

    rutas = pd.read_csv("csv/grafo.csv")
    DG=nx.DiGraph()

    for i in range(17):
        DG.add_node(i)

        
    for row in rutas.iterrows():
        DG.add_edge(row[1]["Origen"],
                    row[1]["Destino"]
                )


    DG.nodes(data=True)
    list(DG.nodes(data=True))
    B=nx.adjacency_matrix(DG)
    B1=B.todense()
    B1=B1-1


    nodo_inicial = start

    nodo_final = end


    size = B1.shape[0]

    for i in range(size):
        if B1[i,nodo_final] != -1:
            B1[i,nodo_final] = 100

    R = B1

    # Q matrix
    Q = np.matrix(np.zeros([size,size]))

    # Gamma (learning parameter).
    gamma = 0.8

    # Initial state. (Usually to be chosen at random)
    initial_state = nodo_inicial

    # This function returns all available actions in the state given as an argument
    def available_actions(state):
        current_state_row = R[state,]
        av_act = np.where(current_state_row >= 0)[1]
        return av_act

    # Get available actions in the current state
    available_act = available_actions(initial_state)

    # This function chooses at random which action to be performed within the range
    # of all the available actions.
    def sample_next_action(available_actions_range):
        next_action = int(np.random.choice(available_act,1))
        return next_action

    # Sample next action to be performed
    action = sample_next_action(available_act)

    # This function updates the Q matrix according to the path selected and the Q
    # learning algorithm
    def update(current_state, action, gamma):

        max_index = np.where(Q[action,] == np.max(Q[action,]))[1]

        if max_index.shape[0] > 1:
            max_index = int(np.random.choice(max_index, size = 1))
        else:
            max_index = int(max_index)
            
        max_value = Q[action, max_index]

        # Q learning formula
        Q[current_state, action] = R[current_state, action] + gamma * max_value

    for i in range(10000):
        current_state = np.random.randint(0, int(Q.shape[0]))
        available_act = available_actions(current_state)
        action = sample_next_action(available_act)
        update(current_state,action,gamma)

    nodo_inicial = start


    current_state = nodo_inicial
    steps = [current_state]

    while current_state != nodo_final:

        next_step_index = np.where(Q[current_state,] == np.max(Q[current_state,]))[1]

        if next_step_index.shape[0] > 1:
            next_step_index = int(np.random.choice(next_step_index, size = 1))
        else:
            next_step_index = int(next_step_index)
        steps.append(next_step_index)
        current_state = next_step_index

    return steps
