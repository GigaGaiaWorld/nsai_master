merge_sort([], []).
merge_sort([X], [X]).
merge_sort(List, Sorted) :-
    length(List, Len),
    Len > 1,
    Half is Len // 2,
    split(List, Half, Left, Right),
    merge_sort(Left, SortedLeft),
    merge_sort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).
split(List, Half, Left, Right) :-
    length(Left, Half),
    append(Left, Right, List).
merge([], Right, Right).
merge(Left, [], Left).
merge([LeftHead|LeftTail], [RightHead|RightTail], [LeftHead|Merged]) :-
    LeftHead =< RightHead,
    merge(LeftTail, [RightHead|RightTail], Merged).
merge([LeftHead|LeftTail], [RightHead|RightTail], [RightHead|Merged]) :-
    LeftHead > RightHead,
    merge([LeftHead|LeftTail], RightTail, Merged).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/