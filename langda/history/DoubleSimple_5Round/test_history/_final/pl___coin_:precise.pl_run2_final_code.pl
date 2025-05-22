PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 

 CNT1 is CNT - 1,
 (coin(CNT) -> coins_r(SC1,S,CNT1), SC1 is SC + 1
 ; coins_r(SC,S,CNT1)).
total(S) :- coins_r(0,S,4).
query(total(_)).

*** Result:*** 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 9:13. 

***Report:***
Validity_form:False\Validity_result:False
The generated code is not valid due to a syntax error in the conditional statement. The '->' operator is incorrectly used, leading to an 'UnknownClause' error. The original code correctly uses a disjunction (;) to handle the probabilistic choice, while the generated code attempts to use a conditional operator which is not supported in this context. The generated code does not meet the requirements and fails to execute.