PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 

    (coin(CNT) -> 
        NewSC is SC + 1,
        NewCNT is CNT - 1,
        coins_r(NewSC, S, NewCNT)
    ; 
        NewCNT is CNT - 1,
        coins_r(SC, S, NewCNT)
    ).
total(S) :- coins_r(0,S,4).
query(total(_)).

*** Result:*** 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 8:16. 

***Report:***
Validity_form:False\Validity_result:False
The generated code attempts to modify the original code by using an 'if-then-else' structure (->/2) which is not valid Problog syntax. This causes a syntax error during execution, making the generated code invalid. The original code correctly uses a disjunction (;) to handle both cases of the coin flip, while the generated code incorrectly tries to use an unsupported conditional operator. The generated code does not produce consistent results with the original code due to this fundamental syntax error.