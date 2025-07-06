insertion_sort([], []).
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).
insert(X, [], [X]).
insert(X, [Y|T], [X,Y|T]) :- X =< Y.
insert(X, [Y|T], [Y|Sorted]) :- X > Y, insert(X, T, Sorted).
 
query(insertion_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in terms of functionality. Both codes implement the insertion sort algorithm in Prolog. The generated code uses slightly different predicate names (insert instead of insert_element) and variable names, but the logic and structure remain the same. The running results of both codes are identical, producing the correct sorted list [1, 2, 3, 5, 7, 12] for the input [3, 1, 2, 5, 7, 12].
*/