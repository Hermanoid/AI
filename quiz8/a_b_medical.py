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

network = {
    "Virus":{
        "Parents": [],
        "CPT": {
            (): 0.01
        }
    },
    "A": {
        "Parents": ["Virus"],
        "CPT": {
            (True,): 0.95,
            (False,): 0.1
        }
    },
    "B": {
        "Parents": ["Virus"],
        "CPT": {
            (True,): 0.9,
            (False,): 0.05
        }
    }
}

if __name__=="__main__":
    answer = query(network, 'Virus', {'A': True})
    print("The probability of carrying the virus\n"
        "if test A is positive: {:.5f}"
        .format(answer[True]))
    answer = query(network, 'Virus', {'B': True})
    print("The probability of carrying the virus\n"
        "if test B is positive: {:.5f}"
        .format(answer[True]))