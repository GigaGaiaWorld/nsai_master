is_sorted([]).
is_sorted([_]).
is_sorted([X,Y|T]) :- X =< Y, is_sorted([Y|T]).

bubble_pass([], []).
bubble_pass([X], [X]).
bubble_pass([X,Y|T], [X|Rest]) :- X =< Y, bubble_pass([Y|T], Rest).
bubble_pass([X,Y|T], [Y|Rest]) :- X > Y, bubble_pass([X|T], Rest).

bubblesort(L, L2) :- is_sorted(L), L2 = L.
bubblesort(L, L2) :- bubble_pass(L, L1), bubblesort(L1, L2).

forth_sort(L, L2) :- bubblesort(L, L2).

query(forth_sort([3,1,2,5,7,12],X)).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for 'bubblesort/3' at 16:21.
*/