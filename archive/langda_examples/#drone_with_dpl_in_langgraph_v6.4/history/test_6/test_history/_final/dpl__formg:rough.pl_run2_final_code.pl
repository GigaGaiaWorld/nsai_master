% Correct Merge Sort Algorithm in Problog

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

% Split the list into two halves accurately
split(List, Left, Right) :-
    length(List, Len),
    Half is Len // 2,
    length(Left, Half),
    append(Left, Right, List).

% Merge two sorted lists into one sorted list with correct comparison logic
merge([], Right, Right).
merge(Left, [], Left).
merge([LeftHead|LeftTail], [RightHead|RightTail], [LeftHead|Merged]) :-
    LeftHead =< RightHead,
    merge(LeftTail, [RightHead|RightTail], Merged).
merge([LeftHead|LeftTail], [RightHead|RightTail], [RightHead|Merged]) :-
    LeftHead > RightHead,
    merge([LeftHead|LeftTail], RightTail, Merged).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code. It implements the merge sort algorithm accurately, including the base cases, recursive splitting, and merging of sorted lists. The logic for splitting and merging is identical to the original code, and the variable names are slightly more descriptive in the generated code. Both codes produce the same correct result when sorting the list [3,1,2,5,7,12].