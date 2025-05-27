PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
coin(C),
    (PH::make_coin(C,PH)), PH=1, NSC is SC + 1 ; NSC = SC,
    NCNT is CNT - 1,
    coins_r(NSC,S,NCNT).
total(S) :- coins_r(0,S,4).
query(total(_)).
/* %%% Result %%% 
Error evaluating Problog model:
    result = self.handle_nonground(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 905, in handle_nonground
    raise NonGroundProbabilisticClause(location=database.lineno(node.location))
problog.engine.NonGroundProbabilisticClause: Encountered a non-ground probabilistic clause at 1:5.
*/