PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
 coin(C), (C -> NSC is SC + 1; NSC is SC), NCNT is CNT - 1, coins_r(NSC,S,NCNT).
total(S) :- coins_r(0,S,4).
query(total(_)).

*** Result:*** 
Error evaluating Problog model:
    result = self.handle_nonground(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 905, in handle_nonground
    raise NonGroundProbabilisticClause(location=database.lineno(node.location))
problog.engine.NonGroundProbabilisticClause: Encountered a non-ground probabilistic clause at 1:5. 

***Report:***
Validity_form:False\Validity_result:False
The generated code is not valid due to a non-ground probabilistic clause error. The issue arises from using a variable 'C' in the 'coin(C)' call without proper instantiation, which is not allowed in probabilistic logic programming. The original code correctly uses 'CNT' as a ground value when calling 'coin(CNT)'. The generated code fails to maintain this crucial aspect, resulting in a runtime error.