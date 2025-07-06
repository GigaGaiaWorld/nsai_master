merge_sort([], []).
merge_sort([X], [X]).
merge_sort(List, Sorted) :-
    List = [_, _ | _],
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
Report: The generated code correctly implements the merge sort algorithm and produces the same result as the original code. The main difference lies in the implementation of the 'split' function, which in the generated code uses pattern matching to divide the list into two halves, while the original code uses 'length' and 'append'. Both approaches are valid and achieve the same goal. The generated code is more concise and potentially more efficient due to its direct pattern matching approach.
*/