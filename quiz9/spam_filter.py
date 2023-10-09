import csv
import numpy as np

def posterior(prior, likelihood, observation):
    def sumup(case):
        return (prior if case else 1-prior) * np.prod(list((l[case] if o else (1-l[case])) for l, o in zip(likelihood, observation)))
    true_case = sumup(True)
    false_case = sumup(False)
    return true_case / (true_case + false_case)

def load(file_name):
    training_data = []
    header = None

    with open(file_name) as in_file:
        first_it = True
        for row in csv.reader(in_file):
            if first_it:
                header = row
                first_it = False
            else:
                training_data.append([int(i) for i in row])
    return np.array(training_data), np.array(header)


def learn_prior(file_name, pseudo_count=0):
    data, header = load(file_name)
    return (sum(row[-1] for row in data) + pseudo_count)/(len(data) + 2*pseudo_count)


def learn_likelihood(file_name, pseudo_count=0):
    data, header = load(file_name)
    # return (np.count_nonzero(data, axis=0) + pseudo_count)/(data.shape[0] + 2*pseudo_count)
    spam_col = data[:,-1]
    return np.column_stack(
        tuple((np.count_nonzero(subset[:, :-1], axis=0) + pseudo_count)/(subset.shape[0] + 2*pseudo_count) for subset in (data[spam_col==0], data[spam_col==1]))
    ).tolist()

def nb_classify(prior, likelihood, observation):
    p = posterior(prior, likelihood, observation)
    return ("Spam" if p > 0.5 else "Not Spam", p if p > 0.5 else 1-p)

if __name__=="__main__":
    print("*** Test Learn Prior")
    prior = learn_prior("spam-labelled.csv")
    print("Prior probability of spam is {:.5f}.".format(prior))

    print("*** Test Learn Likelihood")
    print("Answer structure:")
    likelihood = learn_likelihood("spam-labelled.csv")
    print(len(likelihood))
    print([len(item) for item in likelihood])

    print("X1 values:")
    likelihood = learn_likelihood("spam-labelled.csv")
    print("P(X1=True | Spam=False) = {:.5f}".format(likelihood[0][False]))
    print("P(X1=False| Spam=False) = {:.5f}".format(1 - likelihood[0][False]))
    print("P(X1=True | Spam=True ) = {:.5f}".format(likelihood[0][True]))
    print("P(X1=False| Spam=True ) = {:.5f}".format(1 - likelihood[0][True]))

    likelihood = learn_likelihood("spam-labelled.csv", pseudo_count=1)

    print("With Laplacian smoothing:")
    print("P(X1=True | Spam=False) = {:.5f}".format(likelihood[0][False]))
    print("P(X1=False| Spam=False) = {:.5f}".format(1 - likelihood[0][False]))
    print("P(X1=True | Spam=True ) = {:.5f}".format(likelihood[0][True]))
    print("P(X1=False| Spam=True ) = {:.5f}".format(1 - likelihood[0][True]))

    print("Test Classification")
    prior = learn_prior("spam-labelled.csv")
    likelihood = learn_likelihood("spam-labelled.csv")

    input_vectors = [
        (1,1,0,0,1,1,0,0,0,0,0,0),
        (0,0,1,1,0,0,1,1,1,0,0,1),
        (1,1,1,1,1,0,1,0,0,0,1,1),
        (1,1,1,1,1,0,1,0,0,1,0,1),
        (0,1,0,0,0,0,1,0,1,0,0,0),
        ]

    predictions = [nb_classify(prior, likelihood, vector) 
                for vector in input_vectors]

    for label, certainty in predictions:
        print("Prediction: {}, Certainty: {:.5f}"
            .format(label, certainty))