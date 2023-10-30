import re

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
        yield mo.group('HEAD'), tuple(re.findall(ATOM, mo.group('BODY') or ""))

def forward_deduce(knowledge_base):
    """
    Maybe not the most performant implementation you've ever seen
    """
    kb = set(clauses(knowledge_base))
    proven = set()
    while True:
        to_add = set()
        for c in kb:
            if all((atom in proven) for atom in c[1]):
                to_add.add(c)
        if len(to_add) != 0:
            proven.update([c[0] for c in to_add])
            kb.difference_update(to_add)
        else:
            break

    return proven

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

    print(", ".join(sorted(forward_deduce(kb))))
    



    