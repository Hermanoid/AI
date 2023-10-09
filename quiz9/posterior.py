import numpy as np

def posterior(prior, likelihood, observation):
    def sumup(case):
        return (prior if case else 1-prior) * np.prod(list((l[case] if o else (1-l[case])) for l, o in zip(likelihood, observation)))
    true_case = sumup(True)
    false_case = sumup(False)
    return true_case / (true_case + false_case)


if __name__=="__main__": 
    print("Test 1")
    prior = 0.05
    likelihood = ((0.001, 0.3),(0.05,0.9),(0.7,0.99))

    observation = (True, True, True)

    class_posterior_true = posterior(prior, likelihood, observation)
    print("P(C=False|observation) is approximately {:.5f}"
        .format(1 - class_posterior_true))
    print("P(C=True |observation) is approximately {:.5f}"
        .format(class_posterior_true))  
    
    print("Test 2")
    prior = 0.05
    likelihood = ((0.001, 0.3),(0.05,0.9),(0.7,0.99))

    observation = (True, False, True)

    class_posterior_true = posterior(prior, likelihood, observation)
    print("P(C=False|observation) is approximately {:.5f}"
        .format(1 - class_posterior_true))
    print("P(C=True |observation) is approximately {:.5f}"
        .format(class_posterior_true))  
    
    print ("Test 3")
    prior = 0.05
    likelihood = ((0.001, 0.3),(0.05,0.9),(0.7,0.99))

    observation = (False, False, True)

    class_posterior_true = posterior(prior, likelihood, observation)
    print("P(C=False|observation) is approximately {:.5f}"
        .format(1 - class_posterior_true))
    print("P(C=True |observation) is approximately {:.5f}"
        .format(class_posterior_true)) 
    
    print ("Test 4")
    prior = 0.05
    likelihood = ((0.001, 0.3),(0.05,0.9),(0.7,0.99))

    observation = (False, False, False)

    class_posterior_true = posterior(prior, likelihood, observation)
    print("P(C=False|observation) is approximately {:.5f}"
        .format(1 - class_posterior_true))
    print("P(C=True |observation) is approximately {:.5f}"
        .format(class_posterior_true))  