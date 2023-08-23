/* tear rate related clauses */
normal_tear_rate(RATE) :- RATE >= 5.
low_tear_rate(RATE) :- RATE < 5.

/* age-related clauses */
young(AGE) :- AGE < 45.

/* astigmatic-related clauses */
astigmatic_rec(Recommend, Astigmatic) :-
    Astigmatic = 'yes',
    Recommend = 'hard_lenses';
    Astigmatic = 'no',
    Recommend = 'soft_lenses'.

diagnosis(Recommend, Age, Astigmatic, Tear_Rate) :-
    young(Age),
    normal_tear_rate(Tear_Rate),
    astigmatic_rec(Recommend, Astigmatic).

diagnosis(Recommend, Age, Astigmatic, Tear_Rate) :-
    low_tear_rate(Tear_Rate),
    Recommend = 'no_lenses'.