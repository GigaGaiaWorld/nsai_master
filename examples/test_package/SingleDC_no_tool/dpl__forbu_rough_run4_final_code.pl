bubblesort([], Acc, Acc).
bubblesort(List, Acc, Sorted) :-
    bubble_pass(List, NewList, Flag),
    (Flag == 1 ->
        bubblesort(NewList, Acc, Sorted)
    ;
        append(Acc, NewList, Sorted)
    ).
bubble_pass([X,Y|T], [Y|NewT], 1) :-
    X > Y,
    bubble_pass([X|T], NewT, _).
bubble_pass([X,Y|T], [X|NewT], Flag) :-
    X =< Y,
    bubble_pass([Y|T], NewT, Flag).
bubble_pass([X], [X], 0).
bubble_pass([], [], 0).
forth_sort(L, L2) :- bubblesort(L, [], L2).
query(forth_sort([3,1,2,5,7,12], X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 4:16.
*/