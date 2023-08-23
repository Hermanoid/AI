second(List, X) :- [_,X|_] = List.

swap12([X,Y|T], [Y,X|T]).

listtran([],[]).
listtran([H1|T1], [H2|T2]) :- tran(H1,H2), listtran(T1,T2).

twice([], []).
twice([H1|T1], [H1, H1 | T2]) :- twice(T1, T2).

remove(_, [], []).
remove(X, [Item1 | TailIn], ListOut) :- X = Item1, remove(X, TailIn, ListOut).
remove(X, [Item1 | TailIn], [Item1 | TailOut]) :- X \= Item1, remove(X, TailIn, TailOut).

split_odd_even([], [], []).
split_odd_even([X1, X2 | TailIn], [X1 | TailOut1], [X2 | TailOut2]) :- split_odd_even(TailIn, TailOut1, TailOut2).
split_odd_even([X1 | TailIn], [X1 | TailOut1], ListOut2) :- split_odd_even(TailIn, TailOut1, ListOut2).

% concat([], X, X).
% concat([H1 | T1], L1, [H1 | L2]) :- concat(T1, L1, L2).
preorder(leaf(X), [X]).
preorder(tree(Root, Left, Right), Traversal) :- 
    preorder(Left, LeftTraversal), 
    preorder(Right, RightTraversal), 
    append(LeftTraversal, RightTraversal, LeftRightTraversal),
    Traversal = [Root | LeftRightTraversal].
