% Base case: an empty list or a single-element list is already sorted
merge_sort([], []).
merge_sort([X], [X]).

% Recursive case: split the list, sort the halves, and merge the results
merge_sort(List, Sorted) :-
    List = [_, _ | _], % Ensure the list has at least two elements
    split(List, Left, Right),
    merge_sort(Left, SortedLeft),
    merge_sort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).

% Split the list into two halves
split([], [], []).
split([X], [X], []).
split([X, Y | Tail], [X | Left], [Y | Right]) :-
    split(Tail, Left, Right).

% Merge two sorted lists into one sorted list
merge([], Right, Right).
merge(Left, [], Left).
merge([X | LeftTail], [Y | RightTail], [X | Merged]) :-
    X =< Y,
    merge(LeftTail, [Y | RightTail], Merged).
merge([X | LeftTail], [Y | RightTail], [Y | Merged]) :-
    X > Y,
    merge([X | LeftTail], RightTail, Merged).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality. Both codes implement the merge sort algorithm correctly. The generated code uses a different approach for splitting the list, which is more concise and efficient compared to the original code. The merge and append functions are identical in both codes. The running results of both codes are consistent, producing the same sorted list.