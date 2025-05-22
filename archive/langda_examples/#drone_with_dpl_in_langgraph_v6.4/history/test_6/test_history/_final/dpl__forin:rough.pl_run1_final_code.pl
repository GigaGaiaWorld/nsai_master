% Insertion sort implementation in ProbLog

% Base case: inserting an element into an empty list
insert(X, [], [X]).

% Recursive case: inserting an element into a sorted list
insert(X, [Y|Ys], [X,Y|Ys]) :- X =< Y.
insert(X, [Y|Ys], [Y|Zs]) :- X > Y, insert(X, Ys, Zs).

% Base case: sorting an empty list
insertion_sort([], []).

% Recursive case: sorting a non-empty list
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
The generated code is correct and consistent with the original code. Both implementations of insertion sort follow the same logic: recursively sorting the tail of the list and then inserting the head into the sorted tail. The generated code renames 'insert_element' to 'insert', but the functionality remains identical. The query and its result are also the same in both cases, producing the correct sorted list with a probability of 1.0000.