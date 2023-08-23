% word(astante, a,s,t,a,n,t,e).
% word(astoria, a,s,t,o,r,i,a).
% word(baratto, b,a,r,a,t,t,o).
% word(cobalto, c,o,b,a,l,t,o).
% word(pistola, p,i,s,t,o,l,a).
% word(statale, s,t,a,t,a,l,e).


solution(V1, V2, V3, H1, H2, H3) :-
    word(V1, _, C11, _, C21, _, C31, _),
    word(V2, _, C12, _, C22, _, C32, _),
    word(V3, _, C13, _, C23, _, C33, _),
    word(H1, _, C11, _, C12, _, C13, _),
    word(H2, _, C21, _, C22, _, C23, _),
    word(H3, _, C31, _, C32, _, C33, _).

