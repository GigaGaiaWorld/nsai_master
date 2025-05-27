forth_sort(L, L2) :- bubblesort(L, [], L2).
bubblesort([], Acc, Acc).
bubblesort([H|T], Acc, Sorted) :- bubble(T, H, [Acc], TempList), bubblesort(TempList, [], Sorted).
bubble([], X, Acc, [X|Acc]).
bubble([H|T], X, Acc, Result) :- (X =< H -> bubble(T, H, [X|Acc], Result) ; bubble(T, X, [H|Acc], Result)).
query(forth_sort([3,1,2,5,7,12], X)).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 5:42.
*/