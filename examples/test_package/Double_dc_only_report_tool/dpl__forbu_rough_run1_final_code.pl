bubblesort([], Acc, Acc).
bubblesort([X], Acc, [X|Acc]).
bubblesort([X,Y|Rest], Acc, Sorted) :-
    (X > Y,
     bubblesort([X|Rest], [Y|Acc], Sorted))
    ;
    (X =< Y,
     bubblesort([Y|Rest], [X|Acc], Sorted)).

forth_sort(L, L2) :- bubblesort(L, [], L2).

query(forth_sort([3,1,2,5,7,12], X)).
/* %%% Result %%% 
% Problog Inference Result：
forth_sort([3, 1, 2, 5, 7, 12],[12, 7, 5, 3, 2, 1]) = 1.0000
*/