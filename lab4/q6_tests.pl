q6_test1_answer :-
    directlyIn(irina, natasha),
    writeln('OK').

q6_test2_answer :-
    \+ directlyIn(irina, olga),
    writeln('OK').

q6_test3_answer :-
    contains(katarina, irina),
    writeln('OK').

q6_test4_answer :-
    contains(katarina, natasha),
    writeln('OK').

% Here we look for all of the dolls that contain irina.

q6_test5_answer :-
    findall(P, contains(P, irina), Output),
    sort(Output, SortedOutput),
    foreach(member(X,SortedOutput), (write(X), nl)).