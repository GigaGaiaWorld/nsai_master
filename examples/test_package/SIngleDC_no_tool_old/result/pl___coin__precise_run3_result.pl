PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 

    (coin(CNT) ->
        NSC is SC + 1
    ;
        NSC is SC
    ),
    NCNT is CNT - 1,
    coins_r(NSC,S,NCNT).
total(S) :- coins_r(0,S,4).
query(total(_)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code attempts to simplify the original code by replacing the disjunction with an if-then-else construct (->/2). However, this change introduces a syntax error in Problog, as the '->/2' operator is not correctly used in this context. The original code uses a disjunction (;) to handle both cases of the coin flip, which is the correct approach in Problog. The generated code fails to execute due to this syntax error, making it invalid.
*/