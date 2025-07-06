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

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in functionality. It implements the merge sort algorithm accurately, including the split and merge operations. The only difference is the renaming of the predicate 'split_list' to 'split', which does not affect the logic or outcome. Both codes produce the same sorted list for the given query.
*/