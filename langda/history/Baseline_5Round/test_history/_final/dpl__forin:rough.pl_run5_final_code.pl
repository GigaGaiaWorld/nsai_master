% Base case: sorting an empty list results in an empty list
insertion_sort([], []).

% Recursive case: insert the head into the sorted tail
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).

% Inserting into an empty list creates a single-element list
insert(X, [], [X]).

% Insert X before Y if X =< Y
insert(X, [Y|Rest], [X,Y|Rest]) :-
    X =< Y.

% Otherwise, keep Y and insert X into the rest
insert(X, [Y|Rest], [Y|InsertedRest]) :-
    X > Y,
    insert(X, Rest, InsertedRest).

% Query example
query(insertion_sort([3,1,2,5,7,12],X)).




*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality and logic. Both codes implement the insertion sort algorithm in Prolog, with the same base and recursive cases. The generated code uses slightly different predicate names (insert instead of insert_element) but maintains the same behavior. The running results of both codes are identical, producing the correct sorted list [1, 2, 3, 5, 7, 12] for the input [3, 1, 2, 5, 7, 12].