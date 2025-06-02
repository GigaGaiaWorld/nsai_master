merge_sort([], []).
merge_sort([X], [X]).
merge_sort(List, Sorted) :-
    length(List, Len),
    Len > 1,
    split(List, Left, Right),
    merge_sort(Left, SortedLeft),
    merge_sort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).
split([], [], []).
split([X], [X], []).
split([X, Y | Rest], [X | Left], [Y | Right]) :-
    split(Rest, Left, Right).
merge([], Right, Right).
merge(Left, [], Left).
merge([X | Left], [Y | Right], [X | Merged]) :-
    X =< Y,
    merge(Left, [Y | Right], Merged).
merge([X | Left], [Y | Right], [Y | Merged]) :-
    X > Y,
    merge([X | Left], Right, Merged).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code correctly implements the merge sort algorithm and produces the same result as the original code. The main difference lies in the 'split' function, which in the generated code splits the list by alternating elements between the left and right sublists, whereas the original code splits the list into two halves. Despite this difference in implementation, both versions correctly sort the input list and yield consistent results.
*/