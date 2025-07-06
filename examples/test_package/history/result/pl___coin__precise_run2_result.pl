PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
(coin(CNT), NSC is SC + 1 ; \+coin(CNT), NSC is SC),
    CNT1 is CNT - 1,
    coins_r(NSC,S,CNT1).
total(S) :- coins_r(0,S,4).
query(total(_)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code. The only difference is the use of a new variable 'NSC' instead of 'SC2' in the recursive clause, which does not affect the logic or the results. The generated code maintains the same probabilistic behavior and produces identical results to the original code.
*/