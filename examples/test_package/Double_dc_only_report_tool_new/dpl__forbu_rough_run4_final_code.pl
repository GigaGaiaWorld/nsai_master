bubblesort([], Acc, Acc).
bubblesort([X], Acc, Sorted) :- append([X], Acc, Sorted).
bubblesort([X, Y | Rest], Acc, Sorted) :-
    X =< Y,
    bubblesort([Y | Rest], [X | Acc], Sorted).
bubblesort([X, Y | Rest], Acc, Sorted) :-
    X > Y,
    bubblesort([X | Rest], [Y | Acc], Sorted).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for 'append/3' at 2:33.
*/