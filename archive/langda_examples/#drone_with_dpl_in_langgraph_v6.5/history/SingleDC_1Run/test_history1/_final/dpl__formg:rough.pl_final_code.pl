% Base case: an empty list or a single-element list is already sorted
merge_sort([], []).
merge_sort([X], [X]).

% Recursive case: split the list into two halves, sort each half, and merge the results
merge_sort(List, Sorted) :-
    List = [_, _ | _], % Ensure the list has at least two elements
    split(List, Left, Right),
    merge_sort(Left, SortedLeft),
    merge_sort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).

% Split the list into two halves
split([], [], []).
split([X], [X], []).
split([X, Y | Rest], [X | Left], [Y | Right]) :-
    split(Rest, Left, Right).

% Merge two sorted lists into one sorted list
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

*** Result:*** 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality. Both codes implement the merge sort algorithm and produce the same sorted output for the given input. The generated code uses a different approach for splitting the list, which is more concise and directly splits the list into two halves by alternating elements. This approach is valid and efficient. The merge function and base cases are identical in both codes. The generated code is valid and meets the requirements.