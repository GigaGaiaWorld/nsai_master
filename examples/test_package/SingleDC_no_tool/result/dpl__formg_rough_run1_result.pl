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
merge([L|Left], [R|Right], [L|Merged]) :-
    L =< R,
    merge(Left, [R|Right], Merged).
merge([L|Left], [R|Right], [R|Merged]) :-
    L > R,
    merge([L|Left], Right, Merged).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in terms of functionality. The only difference is the renaming of the predicate 'split_list' to 'split', which does not affect the logic or outcome. Both codes implement merge sort correctly and produce the same sorted result for the given input.
*/