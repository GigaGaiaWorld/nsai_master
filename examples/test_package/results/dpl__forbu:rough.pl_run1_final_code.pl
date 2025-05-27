swap([X, Y | T], true, [Y, X | T]) :- X > Y.
swap([X, Y | T], false, [X, Y | T]) :- X =< Y.

bubble([], [], []).
bubble([X], [], [X]).
bubble([X, Y | T], SwapFlag, [Z | Rest]) :-
    swap([X, Y | T], SwapFlag, [Z | NewT]),
    bubble(NewT, _, Rest).

bubblesort([], Acc, Acc).
bubblesort(L, Acc, Sorted) :-
    bubble(L, SwapFlag, NewL),
    (SwapFlag == true ->
        bubblesort(NewL, Acc, Sorted)
    ;
        append(Acc, NewL, Sorted)
    ).

forth_sort(L, Sorted) :- bubblesort(L, [], Sorted).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 13:23.
*/