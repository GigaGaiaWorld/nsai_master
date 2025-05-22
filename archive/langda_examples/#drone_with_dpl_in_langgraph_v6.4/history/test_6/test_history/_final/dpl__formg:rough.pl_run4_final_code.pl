% Merge Sort in ProbLog

% Base case for an empty list
merge_sort([], []).

% Base case for a single-element list
merge_sort([X], [X]).

% Recursive case: split the list, sort the halves, and merge them
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

% Example query
query(merge_sort([3, 1, 2, 5, 7, 12], X)).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code correctly implements the merge sort algorithm in ProbLog, similar to the original code. It includes base cases for empty and single-element lists, a recursive case for splitting and merging, and a merge predicate. The generated code uses a different approach for splitting the list, which is more concise but functionally equivalent. The running results of both codes are consistent, producing the same sorted list. The generated code is valid and meets the requirements.