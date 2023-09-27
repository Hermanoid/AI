import functools
import operator


def joint_prob(network, assignment):
    return functools.reduce(operator.mul, [p if var_assign else 1-p for var_assign, p in zip(assignment.values(), [network[var]["CPT"][tuple(assignment[parent] for parent in network[var]["Parents"])] for var in assignment])])

if __name__=="__main__":
    print("\nTest 1")
    network = {
        'A': {
            'Parents': [],
            'CPT': {
                (): 0.2
                }},
    }

    p = joint_prob(network, {'A': True})
    print("{:.5f}".format(p))

    print("(skip Test 2)")

    print("\nTest 3:")
    network = {
        'A': {
            'Parents': [],
            'CPT': {
                (): 0.1
                }},
                
        'B': {
            'Parents': ['A'],
            'CPT': {
                (True,): 0.8,
                (False,): 0.7,
                }},
        }
    
    p = joint_prob(network, {'A': False, 'B':True})
    print("{:.5f}".format(p)) 

    print("\nTest 4:")
    network = {
        'A': {
            'Parents': [],
            'CPT': {
                (): 0.1
                }},
                
        'B': {
            'Parents': ['A'],
            'CPT': {
                (True,): 0.8,
                (False,): 0.7,
                }},
        }
    
    p = joint_prob(network, {'A': False, 'B':False})
    print("{:.5f}".format(p))
    p = joint_prob(network, {'A': False, 'B':True})
    print("{:.5f}".format(p))
    p = joint_prob(network, {'A': True, 'B':False})
    print("{:.5f}".format(p))
    p = joint_prob(network, {'A': True, 'B':True})
    print("{:.5f}".format(p)) 

    print("\nTest 5:")

    network = {
        'Burglary': {
            'Parents': [],
            'CPT': {
                (): 0.001
                }},
                
        'Earthquake': {
            'Parents': [],
            'CPT': {
                (): 0.002,
                }},
        'Alarm': {
            'Parents': ['Burglary','Earthquake'],
            'CPT': {
                (True,True): 0.95,
                (True,False): 0.94,
                (False,True): 0.29,
                (False,False): 0.001,
                }},

        'John': {
            'Parents': ['Alarm'],
            'CPT': {
                (True,): 0.9,
                (False,): 0.05,
                }},

        'Mary': {
            'Parents': ['Alarm'],
            'CPT': {
                (True,): 0.7,
                (False,): 0.01,
                }},
        }

    p = joint_prob(network, {'John': True, 'Mary': True,
                            'Alarm': True, 'Burglary': False,
                            'Earthquake': False})
    print("{:.8f}".format(p)) 