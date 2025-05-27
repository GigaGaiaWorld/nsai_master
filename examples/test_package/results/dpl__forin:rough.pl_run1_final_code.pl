insertion_sort(List, Sorted) :- insertion_sort(List, [], Sorted).
insertion_sort([], Acc, Acc).
insertion_sort([H|T], Acc, Sorted) :- insert(H, Acc, NewAcc), insertion_sort(T, NewAcc, Sorted).
insert(X, [], [X]).
insert(X, [Y|Ys], [X,Y|Ys]) :- X =< Y.
insert(X, [Y|Ys], [Y|Zs]) :- X > Y, insert(X, Ys, Zs).
 
query(insertion_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/