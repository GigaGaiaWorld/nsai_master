swap([X, Y | Rest], [Y, X | Rest]) :- X > Y.
swap([X | Rest], [X | RestSwapped]) :- swap(Rest, RestSwapped).

bubble(List, SwappedList) :- swap(List, SwappedList).

bubblesort([], []).
bubblesort([X], [X]).

bubblesort(List, SortedList) :-
    bubble(List, SwappedList),
    (List == SwappedList -> SortedList = List ; bubblesort(SwappedList, SortedList)).

forth_sort(List, SortedList) :- bubblesort(List, SortedList).

query(forth_sort([3,1,2,5,7,12],X)).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 11:26.
*/