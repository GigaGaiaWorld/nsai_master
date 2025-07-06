% Merge Sort in ProbLog

% Base case: empty list is already sorted
merge_sort([], []).

% Single element list is already sorted
merge_sort([X], [X]).

% Recursive case: split, sort halves, then merge
merge_sort(List, Sorted) :-
    length(List, Len),
    Len > 1,
    split(List, Left, Right),
    merge_sort(Left, SortedLeft),
    merge_sort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).

% Split list into two halves
split(List, Left, Right) :-
    length(List, Len),
    Half is Len // 2,
    length(Left, Half),
    append(Left, Right, List).

% Merge two sorted lists
merge([], Right, Right).
merge(Left, [], Left).
merge([L|Ls], [R|Rs], [L|Rest]) :-
    L =< R,
    merge(Ls, [R|Rs], Rest).
merge([L|Ls], [R|Rs], [R|Rest]) :-
    L > R,
    merge([L|Ls], Rs, Rest).

% Helper append predicate
append([], L, L).
append([H|T], L2, [H|R]) :-
    append(T, L2, R).

% Example query
query(merge_sort([3,1,2,5,7,12],X))
.
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is largely correct and consistent with the original code. It implements the merge sort algorithm in ProbLog with the same logic and structure. The only minor issue is the duplicate append predicate and query at the end of the generated code, which is redundant but does not affect functionality. The running results of both codes are identical, producing the correct sorted list.