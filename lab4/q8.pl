% We inverting binary trees today (wooo)

mirror(leaf(X), leaf(Y)) :- X = Y.
mirror(tree(A, B), tree(C, D)) :- mirror(A, D), mirror(B, C). 