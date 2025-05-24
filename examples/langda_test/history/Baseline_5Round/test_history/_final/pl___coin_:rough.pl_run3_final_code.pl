PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
    CNT > 0,
    CNT1 is CNT - 1,
    coin(CNT),
    (make_coin(CNT,PH) -> SC1 is SC + 1; SC1 is SC),
    coins_r(SC1,S,CNT1).
total(S) :- coins_r(0,S,4).

query(total(_)).




*** Result:*** 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 8:24. 

***Report:***
Validity_form:False\Validity_result:False
The generated code is not valid due to a syntax error in the use of the '->' operator, which is not correctly implemented in Problog. The original code uses a disjunction (;) to handle probabilistic choices, while the generated code incorrectly attempts to use a conditional (->). This leads to a runtime error. The generated code does not meet the requirements and fails to produce consistent results with the original code.