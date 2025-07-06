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
merge([L|Ls], [R|Rs], [L|Rest]) :-
    L =< R,
    merge(Ls, [R|Rs], Rest).
merge([L|Ls], [R|Rs], [R|Rest]) :-
    L > R,
    merge([L|Ls], Rs, Rest).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in functionality. Both codes implement the merge sort algorithm in Prolog, with identical base cases, recursive splitting, and merging logic. The generated code refactors the 'split_list' predicate into 'split' with a more direct approach, but the logic remains the same. The merge and append predicates are identical in both versions. The running results of both codes are consistent, producing the same sorted list for the given input.
*/