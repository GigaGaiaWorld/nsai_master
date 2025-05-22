% Merge Sort in ProbLog

% Base case: empty list or single element list is already sorted
merge_sort([], []).
merge_sort([X], [X]).

% Recursive case: split the list, sort the halves, and merge them
merge_sort(List, Sorted) :-
    length(List, Len),
    Len > 1,
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
query(merge_sort([3,1,2,5,7,12], X)).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code correctly implements the merge sort algorithm in ProbLog, similar to the original code. Both versions produce the same sorted output for the given input. The main differences are in the implementation of the 'split' function, where the generated code uses a different approach that splits the list by alternating elements, while the original code splits the list into two halves based on length. Despite this difference, both implementations correctly sort the list and yield consistent results.