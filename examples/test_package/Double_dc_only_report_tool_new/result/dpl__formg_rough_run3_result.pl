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
Report: The generated code is correct and consistent with the original code in terms of functionality and logic. The only difference is the renaming of the predicate 'split_list' to 'split', which does not affect the behavior of the code. Both pieces of code correctly implement the merge sort algorithm and produce the same sorted output for the given input.
*/