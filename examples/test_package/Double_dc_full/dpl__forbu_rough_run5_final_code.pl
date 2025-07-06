bubblesort([], Acc, Acc).
bubblesort(L, Acc, Sorted) :-
    bubble(L, NewL, Last),
    bubblesort(NewL, [Last | Acc], Sorted).

bubble([X], [], X).
bubble([H1, H2 | T], [X1 | T1], X) :-
    (H1 =< H2, X1 = H1, bubble([H2 | T], T1, X)) ;
    (H1 > H2, X1 = H2, bubble([H1 | T], T1, X)).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
forth_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/