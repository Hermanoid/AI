from csp import *
import itertools


csp = CSP(
    var_domains={var: {-1, 0, 1} for var in "abcd"},
    constraints={lambda a, b: a == abs(b), lambda c, d: c > d, lambda a, b, c: a * b > c + 1},
)


def to_relations(csp: CSP):
    for constraint in csp.constraints:
        header = sorted(scope(constraint))
        tuples = set()
        for assignment in itertools.product(*[csp.var_domains[var] for var in header]):
            if satisfies(dict(zip(header, assignment)), constraint):
                tuples.add(assignment)
        yield Relation(header, tuples)


# Too much work for just this problem.
# def eliminate_variable(relations: list[Relation], var: str):
#     """Eliminate the given variable from the given relations."""
#     involved_relations = [r for r in relations if var in r.header]
#     assert len(involved_relations) == 2
#     r1, r2 = involved_relations
#     new_header = sorted(set(r1.header) | set(r2.header) - {var})
#     new_tuples = set()
#     for t1 in r1.tuples:
#         for t2 in r2.tuples:
#             if all(x == y for x, y in zip(t1, t2) if x[0] != var):
#                 new_tuples.add(tuple(x for x in t1 if x[0] != var))

relations = list(to_relations(csp))

r = [
    Relation(header=["c", "d"], tuples={(1, 0), (0, -1), (1, -1)}),
    Relation(header=["a", "b"], tuples={(1, 1), (1, -1), (0, 0)}),
    Relation(header=["a", "b", "c"], tuples={(1, 1, -1), (-1, -1, -1)}),
]

relations_after_elimination = [
    Relation(header=["c", "d"], tuples={(1, 0), (0, -1), (1, -1)}),
    Relation(header=["b", "c"], tuples={(1, -1)}),
]

if __name__ == "__main__":
    relations = list(to_relations(csp))
    print(relations)
