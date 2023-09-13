from csp import *
import itertools

# Original
# crossword_puzzle = CSP(
#     var_domains={
#         # read across:
#         'across1': set("ant big bus car has".split()),
#         'across3': set("book buys hold lane year".split()),
#         'across4': set("ant big bus car has".split()),
#         # read down:
#         'down1': set("book buys hold lane year".split()),
#         'down2': set("ginger search symbol syntax".split()),
#         },
#     constraints={
#         lambda across1, down1: across1[0] == down1[0], # *
#         lambda down1, across3: down1[2] == across3[0], # *
#         lambda across1, down2: across1[2] == down2[0], # *
#         lambda down2, across3: down2[2] == across3[2], # *
#         lambda down2, across4: down2[4] == across4[0], # *
#         })


# Manual GAC
crossword_puzzle = CSP(
    var_domains={
        # read across:
        'across1': set("bus has".split()),                    # 
        'across3': set("lane year".split()),                  # 
        'across4': set("ant car".split()),                    #
        # read down:                                          
        'down1': set("buys hold".split()),                    #
        'down2': set("search syntax".split()),                # 
        },
    constraints={
        lambda across1, down1: across1[0] == down1[0],
        lambda down1, across3: down1[2] == across3[0],
        lambda across1, down2: across1[2] == down2[0],
        lambda down2, across3: down2[2] == across3[2],
        lambda down2, across4: down2[4] == across4[0],
        })

# Original (this doesn't look like it should have a solution)
# canterbury_colouring = CSP(
#     var_domains={
#         'christchurch': {'red', 'green'},
#         'selwyn': {'red', 'green'},
#         'waimakariri': {'red', 'green'},
#         },
#     constraints={
#         lambda christchurch, waimakariri: christchurch != waimakariri,
#         lambda christchurch, selwyn: christchurch != selwyn,
#         lambda selwyn, waimakariri: selwyn != waimakariri,
#         })

# Manual GAC (oh shoot, you can't actually cross any off with arc-consistency)
canterbury_colouring = CSP(
    var_domains={
        'christchurch': {'red', 'green'},
        'selwyn': {'red', 'green'},
        'waimakariri': {'red', 'green'},
        },
    constraints={
        lambda christchurch, waimakariri: christchurch != waimakariri,
        lambda christchurch, selwyn: christchurch != selwyn,
        lambda selwyn, waimakariri: selwyn != waimakariri,
        })


def is_arc_consistent(csp: CSP):
    """Returns True if the given CSP is arc consistent, False otherwise."""
    for var, domain in csp.var_domains.items():
        for x in domain:
            other_vars = [v for v in csp.var_domains if v != var]
            yhat = itertools.product(*[csp.var_domains[v] for v in other_vars])
            constraints = [c for c in csp.constraints if var in scope(c)]
            for constraint in constraints:
                if not any(satisfies({var: x, **dict(zip(other_vars, assignment))}, constraint) for assignment in yhat):
                    return False
    return True

if __name__=="__main__":
    print(sorted(crossword_puzzle.var_domains['across1']))
    print(is_arc_consistent(crossword_puzzle))