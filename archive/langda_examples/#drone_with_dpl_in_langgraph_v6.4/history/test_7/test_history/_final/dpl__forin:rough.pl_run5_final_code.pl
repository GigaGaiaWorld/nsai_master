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
    X =< Y.
insert(X, [Y|T], [Y|SortedT]) :-
    X > Y,
    insert(X, T, SortedT).

% Query example
query(insertion_sort([3,1,2,5,7,12], X)).
 
query(insertion_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality. Both codes implement insertion sort in Prolog with identical logic. The only differences are in variable naming (e.g., 'insert_element' vs 'insert') and minor formatting, which do not affect the behavior. The generated code includes an additional duplicate query line, which is redundant but harmless.