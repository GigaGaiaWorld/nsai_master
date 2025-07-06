insertion_sort([], []).
insertion_sort([Head|Tail], Sorted) :-
    insertion_sort(Tail, SortedTail),
    insert(Head, SortedTail, Sorted).
insert(X, [], [X]).
insert(X, [Y|Tail], [X,Y|Tail]) :-
    X =< Y.
insert(X, [Y|Tail], [Y|SortedTail]) :-
    X > Y,
    insert(X, Tail, SortedTail).
 
query(insertion_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/