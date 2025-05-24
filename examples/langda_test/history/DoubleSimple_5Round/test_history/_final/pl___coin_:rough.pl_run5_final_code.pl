PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 

    coin(C),
    (C -> NSC is SC + 1; NSC is SC),
    NCNT is CNT - 1,
    coins_r(NSC,S,NCNT).
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
The generated code is not correct and does not meet the expectations. The main issue is the non-ground probabilistic clause error, which occurs because the variable 'C' in 'coin(C)' is not properly instantiated before being used in a probabilistic context. This differs from the original code where 'CNT' is used directly in 'coin(CNT)'. The generated code also changes the logic structure by introducing a conditional statement with 'C -> NSC is SC + 1; NSC is SC', which is not equivalent to the original's approach of using separate clauses for success and failure of 'coin(CNT)'. The original code correctly accumulates the count of successful coin flips, while the generated code fails to execute due to the mentioned error.