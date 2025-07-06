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

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in functionality. It successfully implements the merge sort algorithm, splitting the list into halves, recursively sorting them, and then merging the sorted halves. The generated code simplifies the original by inlining the split_list predicate directly into the merge_sort predicate, which does not affect the logic or outcome. Both codes produce the same sorted list for the given query.
*/