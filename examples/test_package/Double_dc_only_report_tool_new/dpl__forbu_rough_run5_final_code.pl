bubblesort([], Acc, Acc).
bubblesort(L, Acc, Sorted) :-
    bubble(L, L1),
    (L = L1 ->
        append(Acc, L, Sorted)
    ;
        append(Acc, [H|T], NewAcc),
        bubblesort(L1, NewAcc, Sorted)
    ).
bubble([X, Y | T], [Y, X | T]) :- X > Y.
bubble([X | T], [X | T1]) :- bubble(T, T1).
forth_sort(L, L2) :- bubblesort(L, [], L2).
query(forth_sort([3,1,2,5,7,12], X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 4:13.
*/