bubblesort([], Acc, Acc).
bubblesort(List, Acc, Sorted) :-
    bubble(List, NewList),
    NewList \= List,
    !,
    bubblesort(NewList, Acc, Sorted).
bubblesort(List, Acc, [List|Acc]).

bubble([X,Y|Rest], [Y|NewRest]) :-
    X > Y,
    !,
    bubble([X|Rest], NewRest).
bubble([X,Y|Rest], [X|NewRest]) :-
    bubble([Y|Rest], NewRest).
bubble([X], [X]).
bubble([], []).

forth_sort(L, L2) :- bubblesort(L, [], L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for '!/0' at 11:5.
*/