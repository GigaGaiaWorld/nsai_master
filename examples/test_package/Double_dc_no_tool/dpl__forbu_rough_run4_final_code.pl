bubblesort([], Acc, Acc).
bubblesort(List, Acc, Sorted) :-
    bubble(List, NewList, Changed),
    (Changed == true ->
        bubblesort(NewList, Acc, Sorted)
    ;
        append(NewList, Acc, Sorted)
    ).

bubble([X,Y|T], [Y|NewT], true) :-
    X > Y,
    bubble([X|T], [X|NewT], _).
bubble([X,Y|T], [X|NewT], Changed) :-
    X =< Y,
    bubble([Y|T], NewT, Changed).
bubble([X], [X], false).
bubble([], [], false).

forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
forth_sort([3, 1, 2, 5, 7, 12],X2) = 0.0000
*/