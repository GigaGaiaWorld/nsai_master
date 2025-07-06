PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
coin(CNT),
    SC1 is SC + 1,
    CNT1 is CNT - 1,
    coins_r(SC1,S,CNT1).
coins_r(SC,S,CNT) :-
    CNT > 0,
    \+ coin(CNT),
    CNT1 is CNT - 1,
    coins_r(SC,S,CNT1).
total(S) :- coins_r(0,S,4).
query(total(_)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and maintains the same functionality as the original code. It effectively separates the two cases of the coin flip (success and failure) into distinct clauses, which improves readability while preserving the logical structure. The running results of both codes are identical, confirming their equivalence in behavior.
*/