merge_sort([], []).
merge_sort([X], [X]).
merge_sort(List, Sorted) :-
    length(List, Len),
    Len > 1,
    split(List, Left, Right),
    merge_sort(Left, SortedLeft),
    merge_sort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).
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
Report: The generated code is correct and consistent with the original code in functionality. The only difference is the renaming of the predicate 'split_list' to 'split', which does not affect the logic or outcome. Both codes implement merge sort correctly, and the running results are identical, producing the same sorted list for the given input.
*/