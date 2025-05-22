PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 

    (coin(CNT) -> NewSC is SC + 1 ; NewSC = SC),
    NewCNT is CNT - 1,
    coins_r(NewSC,S,NewCNT).
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
The generated code attempts to simplify the original code by using an if-then-else construct (->/2), which is not valid in Problog syntax. This causes a syntax error during execution. The original code correctly uses disjunction (;) for probabilistic choice, which is the proper way to handle probabilistic logic in Problog. The generated code fails to maintain the probabilistic nature of the original problem and results in an execution error.