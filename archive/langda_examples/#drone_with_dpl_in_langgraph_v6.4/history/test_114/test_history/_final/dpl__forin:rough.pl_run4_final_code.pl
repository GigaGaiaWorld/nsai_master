% Corrected Insertion Sort in ProbLog

% Base case: an empty list is already sorted
insertion_sort([], []).

% Recursive case: insert the head into the sorted tail
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).

% Insert an element into a sorted list
insert(X, [], [X]).
insert(X, [H|T], [H|SortedT]) :-
    X > H,
    insert(X, T, SortedT).
insert(X, [H|T], [X,H|T]) :-
    X =< H.
 
query(insertion_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality. Both codes implement insertion sort in Prolog and produce the same sorted result for the given input. The generated code has been slightly refactored with renamed predicates (insert_element to insert) and reordered clauses, but the logic remains unchanged. The running results of both codes are identical, confirming their equivalence.