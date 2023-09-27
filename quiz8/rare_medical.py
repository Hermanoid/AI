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
    "Disease": {
        "Parents": [],
        "CPT": {
            (): 1/100000
        }
    },
    "Test": {
        "Parents": ["Disease"],
        "CPT": {
            (True,): 0.99,
            (False,): 0.01
        }
    }
}

if __name__=="__main__":
    answer = query(network, 'Disease', {'Test': True})
    print("The probability of having the disease\n"
        "if the test comes back positive: {:.8f}"
        .format(answer[True]))

    answer = query(network, 'Disease', {'Test': False})
    print("The probability of having the disease\n"
        "if the test comes back negative: {:.8f}"
        .format(answer[True]))