PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
(coin(CNT), NewSC is SC + 1 ; \+ coin(CNT), NewSC = SC),
    CNT1 is CNT - 1,
    coins_r(NewSC,S,CNT1).
total(S) :- coins_r(0,S,4).
query(total(_)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code. It maintains the same logic for counting successful coin flips and produces identical results. The only difference is the renaming of variables (SC2 to NewSC and CNT2 to CNT1), which does not affect the functionality or outcome. The generated code is also syntactically valid and meets the requirements.
*/