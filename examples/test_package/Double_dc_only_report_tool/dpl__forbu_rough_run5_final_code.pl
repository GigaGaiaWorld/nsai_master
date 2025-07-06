bubblesort([], Acc, Acc).
bubblesort(List, Acc, Sorted) :-
    bubble_pass(List, NewList, Swapped),
    (Swapped = true, bubblesort(NewList, Acc, Sorted)
    ;
    (Swapped = false, append(NewList, Acc, Sorted)
    ).
bubble_pass([X, Y | Rest], [Y | NewRest], true) :-
    X > Y,
    bubble_pass([X | Rest], NewRest, _).
bubble_pass([X, Y | Rest], [X | NewRest], Swapped) :-
    X =< Y,
    bubble_pass([Y | Rest], NewRest, Swapped).
bubble_pass([X], [X], false).
bubble_pass([], [], false).
append([], L, L).
append([H | T], L, [H | R]) :-
    append(T, L, R).
forth_sort(L, L2) :-
    bubblesort(L, [], L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
Error evaluating Problog model:
    return self.collapse(string, tokens)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/parser.py", line 1282, in collapse
    raise UnmatchedCharacter(string, expr_stack[-1].start.location)
problog.parser.UnmatchedCharacter: Unmatched character '(' at 4:5.
*/