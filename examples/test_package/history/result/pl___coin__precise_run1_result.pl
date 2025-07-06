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
Report: The generated code attempts to simplify the original code by using a conditional statement (->/2) instead of separate clauses for coin success and failure. However, this approach is syntactically incorrect in Problog, leading to an 'UnknownClause' error. The original code correctly uses separate clauses with disjunction (;), which is the proper way to handle probabilistic choices in Problog. The generated code fails to execute due to this syntax error, making it invalid.
*/