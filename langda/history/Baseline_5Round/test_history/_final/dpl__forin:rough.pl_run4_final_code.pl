% Base case: sorting an empty list results in an empty list
insertion_sort([], []).

% Recursive case: insert the head into the sorted tail
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).

% Inserting into an empty list creates a single-element list
insert(X, [], [X]).

% Insert X at the front if it's smaller than or equal to the head
insert(X, [H|T], [X,H|T]) :-
    X =< H.

% Otherwise, keep the head and insert X into the tail
insert(X, [H|T], [H|SortedTail]) :-
    X > H,
    insert(X, T, SortedTail).

% Query example
query(insertion_sort([3,1,2,5,7,12],X)).




*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in functionality. Both codes implement the insertion sort algorithm in Prolog, with the same logic for sorting and inserting elements. The only difference is the renaming of the predicate 'insert_element' to 'insert' in the generated code, which does not affect the behavior. The running results of both codes are identical, producing the correct sorted list.