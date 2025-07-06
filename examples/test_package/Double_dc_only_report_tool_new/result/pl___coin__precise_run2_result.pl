PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
(coin(CNT), NSC is SC + 1 ; \+ coin(CNT), NSC is SC),
    CNT1 is CNT - 1,
    coins_r(NSC,S,CNT1).
total(S) :- coins_r(0,S,4).
query(total(_)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code. The main difference is the use of a new variable 'NSC' in the generated code instead of 'SC2' in the original code, which does not affect the logic or functionality. Both codes perform the same recursive counting of successful coin flips with a probability of 0.8, and the running results are identical.
*/