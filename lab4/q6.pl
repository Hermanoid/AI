directlyIn(olga, katarina).
directlyIn(natasha, olga).
directlyIn(irina, natasha).
contains(X,Y) :- directlyIn(Y,X).
contains(X,Y) :- directlyIn(Y,Z), contains(X,Z).