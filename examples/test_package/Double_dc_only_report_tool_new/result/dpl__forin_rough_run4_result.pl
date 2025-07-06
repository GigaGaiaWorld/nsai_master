insertion_sort([], []).
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).
insert(X, [], [X]).
insert(X, [Y|Ys], [X,Y|Ys]) :-
    X =< Y.
insert(X, [Y|Ys], [Y|Zs]) :-
    X > Y,
    insert(X, Ys, Zs).
 
query(insertion_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in functionality. Both codes implement the insertion sort algorithm in Prolog. The generated code renames the 'insert_element' predicate to 'insert', but the logic remains the same. The running results of both codes are identical, producing the correct sorted list [1, 2, 3, 5, 7, 12] for the input [3, 1, 2, 5, 7, 12].
*/