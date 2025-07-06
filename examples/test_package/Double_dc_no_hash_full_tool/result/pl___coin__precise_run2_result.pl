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
Report: The generated code is correct and consistent with the original code in terms of functionality and results. The original code uses a single recursive rule with disjunction (;) to handle both coin success and failure cases, while the generated code splits these into two separate rules. This structural difference does not affect the logic or outcome, as both versions correctly model the probabilistic coin flips and counting. The running results are identical, confirming the equivalence of the two implementations.
*/