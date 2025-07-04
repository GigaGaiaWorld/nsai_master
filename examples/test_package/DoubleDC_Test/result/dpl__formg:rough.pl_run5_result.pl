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
split([X, Y | Tail], [X | Left], [Y | Right]) :-
    split(Tail, Left, Right).
merge([], Right, Right).
merge(Left, [], Left).
merge([LeftHead | LeftTail], [RightHead | RightTail], [LeftHead | Merged]) :-
    LeftHead =< RightHead,
    merge(LeftTail, [RightHead | RightTail], Merged).
merge([LeftHead | LeftTail], [RightHead | RightTail], [RightHead | Merged]) :-
    LeftHead > RightHead,
    merge([LeftHead | LeftTail], RightTail, Merged).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in terms of functionality. Both codes implement the merge sort algorithm in Prolog, and they produce the same sorted output for the given input. The main difference lies in the implementation of the 'split' function. The original code uses 'split_list' with 'append', while the generated code uses a recursive 'split' function that alternates elements between the left and right lists. Despite this difference, both approaches correctly split the list for the merge sort algorithm. The generated code is valid and meets the requirements.
*/