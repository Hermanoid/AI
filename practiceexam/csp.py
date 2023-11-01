"""This module provides classes for constructing constraint
satisfaction problem (CSP) objects and some relevant utility
functions. This module is specifically written for COSC367 quizzes at
University of Canterbury.

Author: Kourosh Neshatian
Last modified: 4 Sep 2019

"""

import collections, collections.abc


def scope(constraint):
    """Takes a constraint in the form of a function (or lambda expression)
    and returns the set of formal parameter names.

    """
    return set(constraint.__code__.co_varnames[
        :constraint.__code__.co_argcount])


def satisfies(assignment, constraint):
    """Tests whether the given assignment satisfies the given
    constraint. The assignment is a dictionary of variable names and
    their corresponding values. The constraint is a predicate function
    (or lambda expression). The assignment must contain (at least) all
    the bindings (parameters) required by the constraint.

    """
    return constraint(**{var:val for var,val in assignment.items()
                         if var in scope(constraint)})
                     

class CSP(collections.namedtuple("CSP", "var_domains, constraints")):
    """An instance of a CSP is constructed by specifying a dictionary,
     var_domains, of the form "var_name": set_of_values, and a
     collection of constraints where each constraint is a predicate
     function (i.e. returns either true or false).  The set of CSP variable
     names are implicitly specified by the keys of var_domains. The
     name of the parameters of constraints must be in the set of
     variable names.

    """

    def __init__(self, var_domains, constraints):
        assert type(var_domains) is dict
        assert all(type(name) is str and type(domain) is set
                   for name, domain in var_domains.items())
        assert isinstance(constraints, collections.abc.Iterable)
        assert all(callable(c) and scope(c) <= set(var_domains.keys())
                   for c in constraints)



class Relation(collections.namedtuple("Relation", "header, tuples")):
    """A relation is a like table: it has two components: i) header: a
    sequence of variable names (strings) ii) tuples: a set of rows
    (each of type tuple). The length of each tuple is equal to the
    length of the header (the number of columns in the table). The
    i-th value in the tuple corresponds to the i-th variable in the
    header."""


    def __init__(self, header, tuples):
        assert isinstance(header, collections.abc.Sequence)
        assert all(type(element) is str for element in header)
        assert type(tuples) is set
        assert all(type(element) is tuple for element in tuples)
        assert all(len(tpl) == len(header) for tpl in tuples)

if __name__=="__main__":
    canterbury_colouring = CSP(
    var_domains={
        'christchurch': {'red', 'green'},
        'selwyn': {'red', 'green'},
        'waimakariri': {'red', 'green'},
        },
    constraints={
        lambda christchurch, selwyn, waimakariri: len({christchurch, selwyn, waimakariri}) == 3
        })


    
    
    
import itertools



def relations(csp: CSP):
    r = []
    for constraint in csp.constraints:
        tuples = set()
        variables = sorted(scope(constraint))
        for combination in itertools.product(*(csp.var_domains[var] for var in variables)):
            if satisfies(dict(zip(variables, combination)), constraint):
                tuples.add(combination)
        r.append(Relation(variables, tuples))
    return r

if __name__=="__main__":
    csp = CSP(
    var_domains = {var:{-1,0,1} for var in 'abc'},
    constraints = {
        lambda a, b: a * b == -1,
        lambda b, c: b + c == 1,
        }
    )
    print(relations(csp))