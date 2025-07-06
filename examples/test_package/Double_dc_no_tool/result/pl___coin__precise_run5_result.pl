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
Report: The generated code attempts to simplify the original code by replacing the disjunction with an if-then-else construct. However, it introduces a syntax error in Prolog by using '->' incorrectly, which is not a valid operator in this context. The original code uses a proper disjunction (;)/2 to handle the probabilistic choice, which is correctly interpreted by Problog. The generated code fails to execute due to this syntax error, making it invalid. The original code produces correct probabilistic results for the coin flipping scenario, while the generated code does not run at all.
*/