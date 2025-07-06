bubblesort([], Acc, Acc).
bubblesort(List, Acc, Sorted) :-
    bubble(List, NewList),
    NewList \= List,
    bubblesort(NewList, Acc, Sorted).
bubblesort(List, Acc, Acc) :-
    bubble(List, List).

bubble([X,Y|T], [Y|Rest]) :-
    X > Y,
    bubble([X|T], Rest).
bubble([X,Y|T], [X|Rest]) :-
    X =< Y,
    bubble([Y|T], Rest).
bubble([X], [X]).
bubble([], []).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
forth_sort([3, 1, 2, 5, 7, 12],[]) = 1.0000
*/