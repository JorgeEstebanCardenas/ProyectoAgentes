import json
import numpy as np

# R matrix
def training(Objective = 9):
    
    B1 = np.matrix([
    [ -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,   0,  -1,  -1,  -1],
    [  0,  -1,   0,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1],
    [ -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,   0,  -1,  -1],
    [ -1,  -1,   0,  -1,   0,  -1,  -1,  -1,  -1,  -1,  -1,  -1],
    [ -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,   0,  -1],
    [ -1,  -1,  -1,  -1,   0,  -1,   0,  -1,  -1,  -1,  -1,  -1],
    [ -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,   0],
    [  0,  -1,  -1,  -1,  -1,  -1,   0,  -1,  -1,  -1,  -1,  -1],
    [ -1,  -1,  -1,  -1,  -1,  -1,  -1,   0,  -1,  -1,  -1,   0],
    [ -1,   0,  -1,  -1,  -1,  -1,  -1,  -1,   0,  -1,  -1,  -1],
    [ -1,  -1,  -1,   0,  -1,  -1,  -1,  -1,  -1,   0,  -1,  -1],
    [ -1,  -1,  -1,  -1,  -1,   0,  -1,  -1,  -1,  -1,   0,  -1]
    ])

    for i in range(12):
        if B1[i, Objective] == 0:
            B1[i, Objective] = 100

    # Q matrix
    Q = np.matrix(np.zeros([12,12]))

    # Gamma (learning parameter).
    gamma = 0.8

    # Initial state. (Usually to be chosen at random)
    initial_state = 1
    
    # Get available actions in the current state
    available_act = available_actions(initial_state, B1)
    
    # Sample next action to be performed
    action = sample_next_action(available_act, available_act)
    
    # Update Q matrix
    update(initial_state,action,gamma, B1, Q)
    # Train over 10 000 iterations. (Re-iterate the process above).
    for i in range(10000):
        current_state = np.random.randint(0, int(Q.shape[0]))
        available_act = available_actions(current_state, B1)
        action = sample_next_action(available_act, available_act)
        update(current_state, action, gamma, B1, Q)

    # Normalize the "trained" Q matrix
    #print("Trained Q matrix:")
    #print(Q/np.max(Q)*100)
    #print(Q)
    '''
    newTraining = {
        "LastGoalTrained": Objective,
        "a": {
            "cosas1": 0
        }
    }
    cosas2 = {
        "cosas2": 7
    }
    
    newTraining["a"].append(cosas2)
       
    with open("lastTraining.json", "w") as outfile:
        outfile.write(json.dumps(newTraining))
    
    np.save("trainedMatrix.npy", Q, allow_pickle=True)
    '''
    return Q

# This function returns all available actions in the state given as an argument
def available_actions(state, R):
    current_state_row = R[state,]
    av_act = np.where(current_state_row >= 0)[1]
    return av_act

# This function chooses at random which action to be performed within the range
# of all the available actions.
def sample_next_action(available_actions_range, available_act):
    next_action = int(np.random.choice(available_act,1))
    return next_action

# This function updates the Q matrix according to the path selected and the Q
# learning algorithm
def update(current_state, action, gamma, R, Q):

    max_index = np.where(Q[action,] == np.max(Q[action,]))[1]

    if max_index.shape[0] > 1:
        max_index = int(np.random.choice(max_index, size = 1))
    else:
        max_index = int(max_index)
        
    max_value = Q[action, max_index]

    # Q learning formula
    Q[current_state, action] = R[current_state, action] + gamma * max_value