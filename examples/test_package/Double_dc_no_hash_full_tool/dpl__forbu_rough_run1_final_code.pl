bubble([], [], []).
bubble([X], [], X).
bubble([H1, H2 | T], [X1 | T1], X) :-
    (H1 =< H2,
     X1 = H1,
     bubble([H2 | T], T1, X)
    ;
    (H1 > H2,
     X1 = H2,
     bubble([H1 | T], T1, X)).
forth_sort(L, L2) :- bubblesort(L, [], L2).
bubblesort([], Acc, Acc).
bubblesort(L, Acc, Sorted) :-
    bubble(L, NewL, X),
    bubblesort(NewL, [X | Acc], Sorted).
query(forth_sort([3,1,2,5,7,12], X)).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return self.collapse(string, tokens)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/parser.py", line 1282, in collapse
    raise UnmatchedCharacter(string, expr_stack[-1].start.location)
problog.parser.UnmatchedCharacter: Unmatched character '(' at 4:5.
*/