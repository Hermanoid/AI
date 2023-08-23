word(abalone,a,b,a,l,o,n,e). 
word(abandon,a,b,a,n,d,o,n). 
word(enhance,e,n,h,a,n,c,e). 
word(anagram,a,n,a,g,r,a,m). 
word(connect,c,o,n,n,e,c,t). 
word(elegant,e,l,e,g,a,n,t).

q7_test_answer :-
    findall((V1,V2,V3,H1,H2,H3), solution(V1,V2,V3,H1,H2,H3), L),
    sort(L,S),
    foreach(member(X,S), (write(X), nl)).

q7_test_answer :- write('Wrong answer!').