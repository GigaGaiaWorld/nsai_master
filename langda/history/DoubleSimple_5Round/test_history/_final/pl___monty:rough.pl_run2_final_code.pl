% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).


open_door(D) :-
    select_door(Selected),
    findall(X, (member(X,[1,2,3]), X \= Selected, \+ prize(X)), Doors),
    (   Doors = [A,B] -> 0.5::open_door(A) ; 0.5::open_door(B)
    ;   Doors = [A] -> open_door(A)
    ).

win_keep :-
    select_door(A),
    prize(A).
win_switch :-
    member(A, [1,2,3]),
    \+ select_door(A),
    prize(A),
    \+ open_door(A).
query(prize(_)).
query(select_door(_)).
query(win_keep).
query(win_switch).

*** Result:*** 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 11:23. 

***Report:***
Validity_form:False\Validity_result:False
The generated code attempts to simplify the original Monty Hall problem implementation but introduces syntax errors. The main issue is in the 'open_door' predicate where the conditional operator '->' is incorrectly used, leading to a 'No clauses found' error. The original code correctly handles the probabilistic opening of doors, while the generated version fails to execute due to these syntax issues. The generated code does not maintain the same logical structure or probabilistic behavior as the original.