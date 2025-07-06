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

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in functionality. Both codes implement the merge sort algorithm in Prolog, splitting the list, recursively sorting the sublists, and merging them back together. The generated code refactors the 'split_list' predicate into 'split' with an additional parameter 'Half', which is a minor syntactic change but does not affect the logic or outcome. The merge and append predicates remain identical in both versions. The running results of both codes are consistent, producing the same sorted list.
*/