import functools
import itertools
import operator

def joint_prob(network, assignment):
    return functools.reduce(operator.mul, [p if var_assign else 1-p for var_assign, p in zip(assignment.values(), [network[var]["CPT"][tuple(assignment[parent] for parent in network[var]["Parents"])] for var in assignment])])

def query(network, query_var, evidence):
    hidden_vars = network.keys() - evidence.keys() - {query_var}
    # There is a more efficient implementation for this algorithm. Anyways...
    def summed_prob(case):
        assumption = evidence | {query_var:case}
        return sum(joint_prob(network, assumption | {var: val for var, val in zip(hidden_vars, assignment)}) for assignment in itertools.product((True, False), repeat=len(hidden_vars)))
    ptrue = summed_prob(True)
    pfalse = summed_prob(False)
    p = ptrue/(ptrue+pfalse)
    return {True: p, False: 1-p}


if __name__=="__main__":
    print("Test 1:")
    network = {
        'A': {
            'Parents': [],
            'CPT': {
                (): 0.2
                }},
    }

    answer = query(network, 'A', {})
    print("P(A=true) = {:.5f}".format(answer[True]))
    print("P(A=false) = {:.5f}".format(answer[False]))
    print()

    print("Test 2:")
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
    
    answer = query(network, 'B', {'A': False})
    print("P(B=true|A=false) = {:.5f}".format(answer[True]))
    print("P(B=false|A=false) = {:.5f}".format(answer[False]))
    print()

    print("Test 3:")
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
    
    answer = query(network, 'B', {})
    print("P(B=true) = {:.5f}".format(answer[True]))
    print("P(B=false) = {:.5f}".format(answer[False]))
    print()

    print("Test 4:")
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
    answer = query(network, 'Burglary', {'John': True, 'Mary': True})
    print("Probability of a burglary when both\n"
        "John and Mary have called: {:.3f}".format(answer[True]))
    print()

    print("Test 5:")
    answer = query(network, 'John', {'Mary': True})
    print("Probability of John calling if\n"
        "Mary has called: {:.5f}".format(answer[True]))    
    
    network = {
    'A': {
        'Parents': [],
        'CPT': {
            (): 0.4
            }},

    'B': {
        'Parents': ['A'],
        'CPT': {
            (True,): 0.1,
            (False,): 0.3,
            }},

    'C': {
        'Parents': ['A'],
        'CPT': {
            (True,): 0.2,
            (False,): 0.5,
            }},
    }
    print(query(network, "B", {"C": True}))