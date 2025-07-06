insertion_sort([], []).
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).
insert(X, [], [X]).
insert(X, [Y|T], [X,Y|T]) :-
    X =< Y.
insert(X, [Y|T], [Y|Inserted]) :-
    X > Y,
    insert(X, T, Inserted).
 
query(insertion_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in functionality. Both codes implement the insertion sort algorithm in Prolog. The generated code uses 'insert' instead of 'insert_element' as the predicate name for inserting an element into the sorted list, but the logic remains the same. The running results of both codes are identical, producing the correct sorted list [1, 2, 3, 5, 7, 12] for the input [3, 1, 2, 5, 7, 12].
*/