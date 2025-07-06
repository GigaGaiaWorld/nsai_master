bubblesort([], Acc, Acc).
bubblesort([X], Acc, [X|Acc]).
bubblesort(List, Acc, Sorted) :-
    bubble(List, NewList, Max),
    bubblesort(NewList, [Max|Acc], Sorted).
bubble([X, Y|Rest], [X|NewRest], Max) :-
    X =< Y,
    bubble([Y|Rest], NewRest, Max).
bubble([X, Y|Rest], [Y|NewRest], Max) :-
    X > Y,
    bubble([X|Rest], NewRest, Max).
bubble([X], [], X).
forth_sort(L, L2) :- bubblesort(L, [], L2).
query(forth_sort([3,1,2,5,7,12], X)).
/* %%% Result %%% 
% Problog Inference Result：
forth_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/