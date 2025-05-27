swap([X, Y | T], [Y, X | T]) :- X > Y.
swap([X | T], [X | T1]) :- swap(T, T1).

bubblesort(L, Acc, Sorted) :-
    ( swap(L, L1) ->
        bubblesort(L1, [], Sorted)
    ; 
        append(Acc, L, Sorted)
    ).

forth_sort(L, Sorted) :- bubblesort(L, [], Sorted).

query(forth_sort([3,1,2,5,7,12], X)).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 5:19.
*/