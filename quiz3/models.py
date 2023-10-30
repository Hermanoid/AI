import itertools

def interpretations(atoms):
    atoms = sorted(atoms)
    interpretations_list = []
    
    for values in itertools.product([False, True], repeat=len(atoms)):
        interpretation = {atom: value for atom, value in zip(atoms, values)}
        interpretations_list.append(interpretation)
    
    return interpretations_list


def atoms(formula):
    """Takes a formula in the form of a lambda expression and returns a set of
    atoms used in the formula. The atoms are parameter names represented as
    strings.
    """
    
    return {atom for atom in formula.__code__.co_varnames}
    
def value(formula, interpretation):
    """Takes a formula in the form of a lambda expression and an interpretation
    in the form of a dictionary, and evaluates the formula with the given
    interpretation and returns the result. The interpretation may contain
    more atoms than needed for the single formula.
    """
    arguments = {atom: interpretation[atom] for atom in atoms(formula)}
    return formula(**arguments)

def models(knowledge_base):
    atoms_set = set()
    for formula in knowledge_base:
        atoms_set.update(atoms(formula))
    interpretations_list = interpretations(atoms_set)

    models_list = []
    for interpretation in interpretations_list:
        if all(value(form, interpretation) for form in knowledge_base):
            models_list.append(interpretation)
    
    return models_list

if __name__ == "__main__":
    # knowledge_base = {
    #     lambda a, b: a and not b,
    #     lambda c, d: c or d
    # }
    knowledge_base = {
        lambda p, q: p or not q,
        lambda a, b: a or not b,
        lambda b: b
    }

    for interpretation in models(knowledge_base):
        print(interpretation)