PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
    CNT > 0,
    CNT1 is CNT - 1,
    make_coin(C,0.8),
    (coin(C) -> SC1 is SC + 1 ; SC1 is SC),
    coins_r(SC1,S,CNT1).
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
The generated code is not correct and does not meet the expectations. The main issue is that it introduces a non-ground probabilistic clause, which causes an error during execution. The original code uses a ground probabilistic fact (coin(C)) with a fixed probability, while the generated code attempts to use a non-ground make_coin(C,0.8) directly in the recursive clause, leading to the error. The generated code also changes the logic by introducing a new variable C and using it in a way that is not consistent with the original code's intent.