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
Report: The generated code attempts to simplify the original code by replacing the disjunction with an if-then-else construct (->/2). However, this change introduces a syntax error because Prolog/Problog does not support the ->/2 operator in this context without proper parentheses or in a way that matches its expected usage. The original code correctly uses a disjunction (;) to handle the probabilistic choice, which is essential for Problog's probabilistic reasoning. The generated code fails to execute due to this syntax error, making it invalid for the intended probabilistic computation.
*/