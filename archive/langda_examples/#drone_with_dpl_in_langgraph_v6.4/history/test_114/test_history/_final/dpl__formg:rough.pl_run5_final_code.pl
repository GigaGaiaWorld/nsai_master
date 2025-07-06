% Merge Sort in ProbLog

% Base case for an empty list
merge_sort([], []).

% Base case for a single-element list
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
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code correctly implements the merge sort algorithm in ProbLog, similar to the original code. Both codes produce the same sorted output for the given input. However, the generated code uses a different splitting strategy ('split/3') compared to the original's 'split_list/3'. The new split method directly divides elements alternately into left and right lists, which is more efficient but differs in approach. Both implementations correctly merge and sort the lists, demonstrating functional consistency despite the methodological difference in splitting.