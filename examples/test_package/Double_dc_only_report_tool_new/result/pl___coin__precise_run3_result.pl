PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
P::if(coin(CNT),
        (NewSC is SC + 1,
         NewCNT is CNT - 1,
         coins_r(NewSC,S,NewCNT)),
        (NewCNT is CNT - 1,
         coins_r(SC,S,NewCNT)))
.
total(S) :- coins_r(0,S,4).
query(total(_)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code attempts to use a probabilistic 'if/3' construct which is not recognized in Problog, leading to an 'UnknownClause' error. This makes the generated code invalid as it cannot be executed. The original code correctly uses a disjunction to handle the probabilistic choice, which is the proper approach in Problog. The generated code fails to maintain consistency with the original code's logic and execution.
*/