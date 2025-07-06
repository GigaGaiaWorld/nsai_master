insertion_sort([], []).
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).
insert(X, [], [X]).
insert(X, [H|T], [X,H|T]) :-
    X =< H.
insert(X, [H|T], [H|SortedT]) :-
    X > H,
    insert(X, T, SortedT).
 
query(insertion_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/