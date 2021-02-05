import numpy as np
import random

psi = [1, 0, 0, 0, 0, 0, 0, 0]

program =[
  { "gate": "H", "target_qubits": 1 }, 
  { "gate": "X", "target_qubits": 3 },
  { "gate": "CNOT", "target_qubits": 3 } # here i simulated for first and third as target bits and first qubit as the control
]
 

def get_ground_state(num_qubits):
    # return vector of size 2**num_qubits with all zeroes except first element which is 1
    vector = [1]
    num_qubits = np.power(2,num_qubits)

    for i in range(num_qubits-1):
        i = i +2
        vector.append(0)
    return vector


def get_operator(total_qubits, gate_unitary, target_qubits):

    # return unitary operator of size 2**n x 2**n for given gate and target qubits
    #1. define all the gates that are unitary
    X = np.array([
        [0 ,1],
        [1,0]
    ])

    H = np.array([
        [1/np.sqrt(2), 1/np.sqrt(2)],
        [1/np.sqrt(2), -1/np.sqrt(2)]
    ])
    #get the Idendity matrix
    I = np.identity(2)

   #defining  a CNOT gate Which happens to be a NOT Gate  But controlled
    XX = np.array([
    [0, 1],
    [1, 0]
    ])
    # Define projection operator |0><0|
    P0x0 = np.array([
    [1, 0],
    [0, 0]
    ])
    P1x1 = np.array([
    [0, 0],
    [0, 1]
    ])


    #logic implementation for Matrix operator for single-qubit gates targeting 1,2 or 3 qubits
    if(gate_unitary == "X"):
        
        if(total_qubits == 3 and target_qubits == 3):

            O = np.kron(np.kron(I, I), X)
            return O
        elif(total_qubits == 3 and target_qubits == 2):
            O = np.kron(np.kron(I, X), I)
            return O
        elif( total_qubits == 3 and target_qubits == 1):
            O = np.kron(np.kron(X, I), I)
            return O
        else:
            return
    elif(gate_unitary == "H"):
        if(total_qubits == 3 and target_qubits == 3):

            O = np.kron(np.kron(I, I), H)
            return O 
        elif(total_qubits == 3 and target_qubits == 2):
            O = np.kron(np.kron(I, H), I)
            return O
        elif( total_qubits == 3 and target_qubits == 1):
            O = np.kron(np.kron(H, I), I)
            return O
        else:
            return
    elif(gate_unitary == "CNOT"):
        #first qubit as control and third qubit as target in 3 qubit quantum circuit
        if(total_qubits == 3 and target_qubits == 3):
            O = np.kron(np.kron(P0x0, I), I) + np.kron(np.kron(P1x1, I), XX)
            return O
        # acting on first and second qubit for a 3 qubit quantum circuit
        elif(total_qubits == 3 and target_qubits == 1):
            O = np.kron(np.kron(P0x0, XX), XX) + np.kron(np.kron(P1x1, XX), I)
            return O
    else:
        return
    

def run_program(initial_state, program):

    # read program, and for each gate:
    gate = program[2]["gate"]
    targetqubits = (program[2]["target_qubits"])
       
     #   - calculate matrix operator
    total_qubits = 3  #from initial state i should calculate the total number of qbits
    operator = get_operator(total_qubits,gate,targetqubits)
    #   - multiply state with operator
    finalState = np.dot(operator,initial_state)
    # return final state

    return finalState


final_state = (run_program(psi,program))


def measure_all(state_vector):
    # choose element from state_vector using weighted random and return it's index
    X = random.randrange(0,3)
    return state_vector[X]





def get_counts(state_vector, num_shots):
    numberofStateHigh = 0
    numberOfStateLow  = 0

    results = [
        {"11":0},
        {"00":0},
    ]
    

    for i in range(num_shots):
        seleted_state = (measure_all(final_state))
        i = i+2

        if(seleted_state == 0.0):
            numberOfStateLow = numberOfStateLow+1
            results[1]["00"] =  numberOfStateLow
        else:
            numberofStateHigh = numberofStateHigh+1
            results[0]["11"] = numberofStateHigh
        
    return results


print(get_counts(final_state,100))