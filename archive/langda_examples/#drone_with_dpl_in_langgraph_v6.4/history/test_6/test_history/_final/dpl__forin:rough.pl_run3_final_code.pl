% Insertion Sort in ProbLog

% Base case: inserting an element into an empty list
insert(X, [], [X]).

% Recursive case: insert X into the sorted list [Y|Ys]
insert(X, [Y|Ys], [X,Y|Ys]) :- X =< Y.
insert(X, [Y|Ys], [Y|Zs]) :- X > Y, insert(X, Ys, Zs).

% Base case: an empty list is already sorted
insertion_sort([], []).

% Recursive case: sort the tail and insert the head into the sorted tail
insertion_sort([X|Xs], Sorted) :-
    insertion_sort(Xs, SortedTail),
    insert(X, SortedTail, Sorted).

% Query example
query(insertion_sort([3,1,2,5,7,12], X)).
 
query(insertion_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code. Both codes implement insertion sort in Prolog with identical logic. The generated code renames 'insert_element' to 'insert' but maintains the same functionality. The query and results are exactly the same, producing the correct sorted list with a probability of 1.0000.