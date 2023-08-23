eats(X, Y):-likes(X, Y).

eats(X, Y) :- edible(Y), hungry(X).
