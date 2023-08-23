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

q3_test1_answer :-
    listtran(X, [one, seven, six, two]),
    writeln(X).

q3_test2_answer :-
    listtran([tahi], [one, eight]),
    writeln('The predicate should not succeed for lists of different lengths!').

q3_test2_answer :-
    writeln('OK').

tran(eins,1). 
tran(zwei,2). 
tran(drei,3). 
tran(vier,4). 
tran(fuenf,5). 
tran(sechs,6). 
tran(sieben,7). 
tran(acht,8). 
tran(neun,9).

q3_test3_answer :-
    listtran([eins, neun, zwei], X),
    writeln(X).


q4_test1_answer :-
    twice(L, [1, 1, 2, 2, 3, 3]),
    writeln(L).

q5_test1_answer :-
    remove(term2, [term1, term2, term3], [term1, term3]),
    write('OK').

q6_test1_answer :-
    split_odd_even([a,b,c,d,e,f,g], A, B),
    write(A),
    writeln(B).

q6_test2_answer :-
    split_odd_even([1,2,3,5], A, B),
    write(A),
    writeln(B).

q7_test3_answer :- preorder(tree(a, tree(b, leaf(c), leaf(d)), leaf(e)), T), 
               writeln(T).