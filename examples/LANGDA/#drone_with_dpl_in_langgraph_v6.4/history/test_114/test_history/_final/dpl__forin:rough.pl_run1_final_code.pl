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
The generated code is correct and consistent with the original code in terms of functionality. Both codes implement insertion sort in Prolog with identical logic. The generated code renames the 'insert_element' predicate to 'insert', but this does not affect the functionality. The query and the result are the same in both cases, producing the correct sorted list. There are no problems with the generated code.