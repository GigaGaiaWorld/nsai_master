merge_sort([], []).
merge_sort([X], [X]).
merge_sort(List, Sorted) :-
    length(List, Len),
    Len > 1,
    Half is Len // 2,
    length(FirstHalf, Half),
    append(FirstHalf, SecondHalf, List),
    merge_sort(FirstHalf, SortedFirst),
    merge_sort(SecondHalf, SortedSecond),
    merge(SortedFirst, SortedSecond, Sorted).
merge([], L, L).
merge(L, [], L).
merge([X|Xs], [Y|Ys], [X|Zs]) :-
    X =< Y,
    merge(Xs, [Y|Ys], Zs).
merge([X|Xs], [Y|Ys], [Y|Zs]) :-
    X > Y,
    merge([X|Xs], Ys, Zs).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/