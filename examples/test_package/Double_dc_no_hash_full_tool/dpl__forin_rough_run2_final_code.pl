insertion_sort(List, Sorted) :- insertion_sort(List, [], Sorted).
insertion_sort([], Sorted, Sorted).
insertion_sort([H|T], Acc, Sorted) :- insert(H, Acc, NewAcc), insertion_sort(T, NewAcc, Sorted).
insert(X, [], [X]).
insert(X, [Y|T], [X,Y|T]) :- X =< Y.
insert(X, [Y|T], [Y|NewT]) :- X > Y, insert(X, T, NewT).
 
query(insertion_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/