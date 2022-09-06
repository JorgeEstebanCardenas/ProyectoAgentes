import json
import numpy as np
from training import training

def matrix_search(start, end):
    steps = [start]
    '''
    with open('lastTraining.json', 'r') as openfile:
        json_object = json.load(openfile)
        
    if(end == json_object['LastGoalTrained']):
        Q = np.load("trainedMatrix.npy", allow_pickle=True)
    else:
        Q = training(end)
    '''

    Q = training(end)
    
    while start != end:

        next_step_index = np.where(Q[start,] == np.max(Q[start,]))[1]

        if next_step_index.shape[0] > 1:
            next_step_index = int(np.random.choice(next_step_index, size = 1))
        else:
            next_step_index = int(next_step_index)
        steps.append(next_step_index)
        start = next_step_index

    # Print selected sequence of steps
    return steps