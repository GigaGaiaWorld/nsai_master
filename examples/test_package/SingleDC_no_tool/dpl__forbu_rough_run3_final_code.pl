bubblesort([], Acc, Acc).
bubblesort(List, Acc, Sorted) :-
    bubble(List, NewList, Swapped),
    (Swapped == true ->
        bubblesort(NewList, Acc, Sorted)
    ; 
        append(NewList, Acc, Sorted)
    ).

bubble([X,Y|T], [Y|NT], true) :- 
    X > Y, 
    bubble([X|T], NT, _).
bubble([X,Y|T], [X|NT], Swapped) :- 
    X =< Y, 
    bubble([Y|T], NT, Swapped).
bubble([X], [], false).
bubble([], [], false).

forth_sort(L, L2) :- bubblesort(L, [], L2).

query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 4:22.
*/