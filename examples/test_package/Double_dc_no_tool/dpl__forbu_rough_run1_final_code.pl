bubblesort([], Acc, Acc).
bubblesort([X], Acc, [X|Acc]).
bubblesort([X,Y|Rest], Acc, Sorted) :-
    (X > Y) ->
        bubblesort([X|Rest], [Y|Acc], Sorted)
    ;
        bubblesort([Y|Rest], [X|Acc], Sorted)
    ).

forth_sort(L, L2) :- bubblesort(L, [], L2).

query(forth_sort([3,1,2,5,7,12], X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return self.collapse(string, tokens)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/parser.py", line 1262, in collapse
    raise UnmatchedCharacter(string, token.location)
problog.parser.UnmatchedCharacter: Unmatched character ')' at 8:5.
*/