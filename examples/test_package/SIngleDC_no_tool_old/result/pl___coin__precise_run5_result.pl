PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
(coin(CNT) -> NSC is SC + 1 ; NSC = SC),
    CNT1 is CNT - 1,
    coins_r(NSC,S,CNT1).
total(S) :- coins_r(0,S,4).
query(total(_)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code attempts to simplify the original code by using a conditional statement (->) instead of separate clauses with disjunction (;). However, this approach is syntactically incorrect in Problog, leading to an 'UnknownClause' error. The original code correctly uses disjunction to handle probabilistic choices, while the generated code fails to maintain this structure. The generated code is not valid Problog syntax and does not produce the expected results.
*/