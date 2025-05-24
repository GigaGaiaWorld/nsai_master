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

*** Result:*** 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 8:13. 

***Report:***
Validity_form:False\Validity_result:False
The generated code attempts to simplify the original code by using a conditional statement (->) instead of separate clauses with disjunction (;). However, this approach is syntactically incorrect in Problog, leading to an 'UnknownClause' error. The original code correctly uses disjunction to handle both cases of coin toss outcomes, while the generated code fails to adhere to Problog's syntax rules for probabilistic logic programming.