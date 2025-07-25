%% Insertion Sort in ProbLog

% Base case: sorting an empty list results in an empty list
insertion_sort([], []).

% Recursive case: insert the head into the sorted tail
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).

% Inserting into an empty list
insert(X, [], [X]).

% Inserting into a non-empty list
insert(X, [Y|Ys], [X,Y|Ys]) :-
    X =< Y.
insert(X, [Y|Ys], [Y|Zs]) :-
    X > Y,
    insert(X, Ys, Zs).

% Query example
query(insertion_sort([3,1,2,5,7,12],X)).
 
query(insertion_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality. Both codes implement insertion sort in Prolog with identical logic. The only differences are in variable naming (e.g., 'insert_element' vs 'insert') and minor formatting, which do not affect the behavior. The generated code produces the same correct sorting result as the original code.