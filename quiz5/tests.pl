q1_test1_answer :-
    second([cosc, 2, Var, beethoven], X),
    writeln(X).

q1_test2_answer :-
    \+ second([1], X),
    writeln('OK').

q1_test3_answer :-
    second([_],_),
    writeln('The predicate should fail on lists of length one!').

q1_test4_answer :-
    second([a, b, c, d], b),
    writeln('OK').

q1_test5_answer :-
    second(L, X),
    writeln('OK').

q2_test1_answer :-
    swap12([a, b, c, d], L),
    writeln(L).

tran(tahi,one). 
tran(rua,two). 
tran(toru,three). 
tran(wha,four). 
tran(rima,five). 
tran(ono,six). 
tran(whitu,seven). 
tran(waru,eight). 
tran(iwa,nine).