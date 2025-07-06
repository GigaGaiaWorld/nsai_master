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

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code. It performs the same merge sort operation, with only minor syntactic differences such as variable naming and predicate naming (e.g., 'split_list' vs 'split'). The logic and functionality remain unchanged, and the running results are identical.
*/