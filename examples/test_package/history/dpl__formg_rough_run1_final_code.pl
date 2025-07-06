merge_sort([], []).
merge_sort([X], [X]).
merge_sort(List, Sorted) :-
    length(List, Len),
    Len > 1,
    split(List, Left, Right),
    merge_sort(Left, LeftSorted),
    merge_sort(Right, RightSorted),
    merge(LeftSorted, RightSorted, Sorted).
split(List, Left, Right) :-
    length(List, Len),
    Half is Len // 2,
    length(Left, Half),
    append(Left, Right, List).
merge([], Right, Right).
merge(Left, [], Left).
merge([LeftH|LeftT], [RightH|RightT], [LeftH|Rest]) :-
    LeftH =< RightH,
    merge(LeftT, [RightH|RightT], Rest).
merge([LeftH|LeftT], [RightH|RightT], [RightH|Rest]) :-
    LeftH > RightH,
    merge([LeftH|LeftT], RightT, Rest).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/