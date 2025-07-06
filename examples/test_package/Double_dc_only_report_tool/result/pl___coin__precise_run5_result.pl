PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
CNT1 is CNT - 1,
    (coin(CNT) -> SC1 is SC + 1 ; SC1 = SC),
    coins_r(SC1,S,CNT1).
total(S) :- coins_r(0,S,4).
query(total(_)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code attempts to simplify the original code by using an if-then-else construct (->/2), but it introduces a syntax error. Problog does not recognize the '->' operator in this context, leading to an 'UnknownClause' error. The original code correctly uses disjunction (;) for probabilistic choice, which is the proper way to handle probabilistic logic in Problog. The generated code fails to execute due to this syntax issue, making it invalid.
*/