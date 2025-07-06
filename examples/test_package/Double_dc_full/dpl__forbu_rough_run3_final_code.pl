bubblesort(List, Sorted) :- bubblesort(List, [], Sorted).
bubblesort([], Acc, Acc).
bubblesort([H|T], Acc, Sorted) :- bubble(H, T, NT, Max), bubblesort(NT, [Max|Acc], Sorted).
bubble(X, [], [], X).
bubble(X, [Y|T], [X|NT], Max) :- X =< Y, bubble(Y, T, NT, Max).
bubble(X, [Y|T], [Y|NT], Max) :- X > Y, bubble(X, T, NT, Max).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
forth_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/