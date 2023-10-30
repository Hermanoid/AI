import re
from search import *


def clauses(knowledge_base):
    """Takes the string of a knowledge base; returns an iterator for pairs
    of (head, body) for propositional definite clauses in the
    knowledge base. Atoms are returned as strings. The head is an atom
    and the body is a (possibly empty) list of atoms.

    -- Kourosh Neshatian - 2 Aug 2021

    """
    ATOM   = r"[a-z][a-zA-Z\d_]*"
    HEAD   = rf"\s*(?P<HEAD>{ATOM})\s*"
    BODY   = rf"\s*(?P<BODY>{ATOM}\s*(,\s*{ATOM}\s*)*)\s*"
    CLAUSE = rf"{HEAD}(:-{BODY})?\."
    KB     = rf"^({CLAUSE})*\s*$"

    assert re.match(KB, knowledge_base)

    for mo in re.finditer(CLAUSE, knowledge_base):
        yield mo.group('HEAD'), re.findall(ATOM, mo.group('BODY') or "")


class KBGraph(Graph):
    def __init__(self, kb, query):
        self.clauses = list(clauses(kb))
        self.atom_expansions = {}
        for clause in self.clauses:
            if clause[0] not in self.atom_expansions:
                self.atom_expansions[clause[0]] = []
            self.atom_expansions[clause[0]].append(clause[1])
        self.query = query

    def starting_nodes(self):
        return [list(self.query)]
        
    def is_goal(self, node):
        return len(node) == 0

    def outgoing_arcs(self, tail_node):
        atom_to_expand = tail_node[0]
        expansions = self.atom_expansions.get(atom_to_expand, [])
        to_return = []
        for expansion in expansions:
            new_node = expansion + tail_node[1:]
            action = ""
            if len(expansion) == 0:
                action = f"Atom {atom_to_expand} is given"
            else:
                expansion_str = ", ".join(expansion)
                action = f"Expand {atom_to_expand} into {expansion_str}"
            to_return.append(Arc(tail_node, new_node, action=action, cost=1))
        return to_return

class DFSFrontier(Frontier):
    """Implements a frontier container appropriate for depth-first
    search."""

    def __init__(self):
        """The constructor takes no argument. It initialises the
        container to an empty stack."""
        self.container = []

    def add(self, path):
        self.container.append(path)

    def __iter__(self):
        """The object returns itself because it is implementing a __next__
        method and does not need any additional state for iteration."""
        return self
        
    def __next__(self):
        if len(self.container) > 0:
            return self.container.pop()
        else:
            raise StopIteration   # don't change this one

if __name__ == "__main__":
    kb = """
    a :- b, c.
    b :- d, e.
    b :- g, e.
    c :- e.
    d.
    e.
    f :- a,
        g.
    """

    query = {'a', 'b', 'd'}
    solution = next(generic_search(KBGraph(kb, query), DFSFrontier()), None)
    if solution:
        print_actions(solution)
        print("The query is true.")
    else:
        print("The query is not provable.")