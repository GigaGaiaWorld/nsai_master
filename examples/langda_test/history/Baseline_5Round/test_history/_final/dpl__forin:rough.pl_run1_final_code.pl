% Base case: sorting an empty list results in an empty list
insertion_sort([], []).

% Recursive case: insert the head into the sorted tail
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).

% Inserting into an empty list
insert(X, [], [X]).

% Inserting into a non-empty list
insert(X, [H|T], [X,H|T]) :- X =< H.
insert(X, [H|T], [H|Inserted]) :- X > H, insert(X, T, Inserted).

% Query example
query(insertion_sort([3,1,2,5,7,12],X)).




*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality. Both codes implement the insertion sort algorithm in Prolog, with the same logic for sorting and inserting elements. The only difference is the renaming of the predicate 'insert_element' to 'insert' in the generated code, which does not affect the behavior. The running results of both codes are identical, producing the same sorted list.