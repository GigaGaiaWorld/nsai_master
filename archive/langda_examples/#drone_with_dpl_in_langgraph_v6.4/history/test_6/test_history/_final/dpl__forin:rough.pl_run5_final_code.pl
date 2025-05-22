% Insertion Sort in ProbLog

% Base case: inserting an element into an empty list results in a list with that element.
insert(X, [], [X]).

% Recursive case: insert X into the sorted list [Y|Ys].
% If X <= Y, insert X at the front; otherwise, insert X into Ys.
insert(X, [Y|Ys], [X,Y|Ys]) :- X =< Y.
insert(X, [Y|Ys], [Y|Zs]) :- X > Y, insert(X, Ys, Zs).

% Base case: sorting an empty list results in an empty list.
insertion_sort([], []).

% Recursive case: sort the list [X|Xs] by inserting X into the sorted version of Xs.
insertion_sort([X|Xs], Sorted) :-
    insertion_sort(Xs, SortedXs),
    insert(X, SortedXs, Sorted).

% Query example
query(insertion_sort([3,1,2,5,7,12], X)).
 
query(insertion_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code. Both codes implement insertion sort in Prolog with identical logic. The generated code renames 'insert_element' to 'insert' but maintains the same functionality. The query and results are exactly the same, producing the correct sorted list with a probability of 1.0000.