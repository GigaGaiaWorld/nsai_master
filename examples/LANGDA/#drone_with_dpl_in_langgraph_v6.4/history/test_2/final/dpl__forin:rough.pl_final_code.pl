% Insertion Sort in ProbLog

% Base case: inserting an element into an empty list
insert(X, [], [X]).

% Recursive case: inserting an element into a sorted list
insert(X, [Y|Ys], [X,Y|Ys]) :- X @=< Y.
insert(X, [Y|Ys], [Y|Zs]) :- X @> Y, insert(X, Ys, Zs).

% Base case: sorting an empty list
insertion_sort([], []).

% Recursive case: sorting a non-empty list
insertion_sort([X|Xs], Sorted) :-
    insertion_sort(Xs, SortedXs),
    insert(X, SortedXs, Sorted).

% Query example
query(insertion_sort([3,1,2,5,7,12], X))
.
 
query(insertion_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 12, 2, 3, 5, 7]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:False
The generated code is structurally similar to the original code, implementing insertion sort in Prolog. However, there are two issues: 1) The generated code contains a duplicate query at the end, which is unnecessary. 2) More importantly, the sorting result is incorrect ([1, 12, 2, 3, 5, 7] instead of [1, 2, 3, 5, 7, 12]), indicating a logical error in the sorting implementation. The comparison operators (@=< and @>) are correctly used, but the sorting algorithm isn't working as intended.