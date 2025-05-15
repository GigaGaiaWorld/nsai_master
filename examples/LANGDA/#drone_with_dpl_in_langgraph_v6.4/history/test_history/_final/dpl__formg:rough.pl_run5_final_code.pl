% Merge Sort in ProbLog

% Base case for empty list
merge_sort([], []).

% Base case for single element list
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
merge([X | LeftTail], [Y | RightTail], [X | MergedTail]) :-
    X =< Y,
    merge(LeftTail, [Y | RightTail], MergedTail).
merge([X | LeftTail], [Y | RightTail], [Y | MergedTail]) :-
    X > Y,
    merge([X | LeftTail], RightTail, MergedTail).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code correctly implements the merge sort algorithm in ProbLog, similar to the original code. Both codes handle base cases and recursive sorting with merging. The generated code uses a different splitting approach ('split/3') compared to the original's 'split_list/3', but both achieve the same goal of dividing the list into two halves. The merging logic is identical in both codes. The generated code is valid and produces the same correct sorting result as the original code.