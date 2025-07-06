merge_sort([], []).
merge_sort([X], [X]).
merge_sort(List, Sorted) :-
    List = [_, _ | _],
    split(List, Left, Right),
    merge_sort(Left, SortedLeft),
    merge_sort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).
split([], [], []).
split([X], [X], []).
split([X, Y | Rest], [X | Left], [Y | Right]) :-
    split(Rest, Left, Right).
merge([], L, L).
merge(L, [], L).
merge([X | Xs], [Y | Ys], [X | Zs]) :-
    X =< Y,
    merge(Xs, [Y | Ys], Zs).
merge([X | Xs], [Y | Ys], [Y | Zs]) :-
    X > Y,
    merge([X | Xs], Ys, Zs).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/