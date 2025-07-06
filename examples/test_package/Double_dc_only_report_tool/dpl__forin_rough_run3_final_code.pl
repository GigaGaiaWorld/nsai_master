insertion_sort(List, SortedList) :- insertion_sort(List, [], SortedList).
insertion_sort([], Acc, Acc).
insertion_sort([H|T], Acc, SortedList) :- insert(H, Acc, NewAcc), insertion_sort(T, NewAcc, SortedList).
insert(X, [], [X]).
insert(X, [Y|T], [X,Y|T]) :- X =< Y.
insert(X, [Y|T], [Y|NewT]) :- X > Y, insert(X, T, NewT).
 
query(insertion_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/