import itertools

def interpretations(atoms):
    atoms = sorted(atoms)
    interpretations_list = []
    
    for values in itertools.product([False, True], repeat=len(atoms)):
        interpretation = {atom: value for atom, value in zip(atoms, values)}
        interpretations_list.append(interpretation)
    
    return interpretations_list

if __name__ == "__main__":
    # Example usage
    atoms = {'A', 'B', 'C'}
    interpretations_list = interpretations(atoms)
    for interpretation in interpretations_list:
        print(interpretation)