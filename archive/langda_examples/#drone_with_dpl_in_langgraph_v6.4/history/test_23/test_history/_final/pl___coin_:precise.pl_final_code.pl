PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 

    CNT1 is CNT - 1,
    (coin(CNT) ->
        SC1 is SC + 1,
        coins_r(SC1, S, CNT1)
    ;
        coins_r(SC, S, CNT1)
    ).
total(S) :- coins_r(0,S,4).
query(total(_)).

*** Result:*** 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 9:16. 

***Report:***
Validity_form:False\Validity_result:False
The generated code attempts to replicate the functionality of the original code but introduces a syntax error by using the '->' operator incorrectly. The original code uses a disjunction (;) to handle both cases of the coin flip, while the generated code incorrectly tries to use an if-then-else construct without proper syntax. This leads to a runtime error indicating that no clauses were found for the '->/2' operator. The generated code is not valid and does not produce consistent results with the original code.