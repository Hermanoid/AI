second(List, X) :- [_,X|_] = List.

swap12([X,Y|T], [Y,X|T]).