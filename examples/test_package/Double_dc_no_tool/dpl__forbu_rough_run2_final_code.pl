bubblesort([], Acc, Acc).
bubblesort([X], Acc, Sorted) :- 
    append(Acc, [X], Sorted).
bubblesort(List, Acc, Sorted) :-
    bubble_pass(List, NewList, Swapped),
    (Swapped == true ->
        bubblesort(NewList, Acc, Sorted)
    ;
        append(Acc, NewList, Sorted)
    ).

bubble_pass([X,Y|Rest], [Y|NewRest], true) :-
    X > Y,
    bubble_pass([X|Rest], NewRest, _).
bubble_pass([X,Y|Rest], [X|NewRest], Swapped) :-
    X =< Y,
    bubble_pass([Y|Rest], NewRest, Swapped).
bubble_pass([X], [X], false).
bubble_pass([], [], false).

forth_sort(L,L2) :- bubblesort(L,[],L2).

query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 6:22.
*/