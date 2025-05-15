% Insertion Sort in ProbLog

% Base case: an empty list is already sorted
insertion_sort([], []).

% Recursive case: insert the head into the sorted tail
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).

% Insert an element into a sorted list
insert(X, [], [X]).
insert(X, [Y|T], [X,Y|T]) :-
    X @=< Y.
insert(X, [Y|T], [Y|SortedT]) :-
    X @> Y,
    insert(X, T, SortedT).
 
query(insertion_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 12, 2, 3, 5, 7]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:False
The generated code is structurally similar to the original code but uses different predicate names ('insert' instead of 'insert_element') and comparison operators ('@=<' and '@>' instead of '=<' and '>'). While the generated code is syntactically correct and meets the requirements (Validity_form is true), the running result is incorrect. The sorted list [1, 12, 2, 3, 5, 7] is not correctly ordered, indicating a logical error in the implementation. This inconsistency makes Validity_result false.