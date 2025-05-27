insertion_sort([], []).
insertion_sort([Head|Tail], Sorted) :-
    insertion_sort(Tail, SortedTail),
    insert(Head, SortedTail, Sorted).
insert(X, [], [X]).
insert(X, [Y|Ys], [X,Y|Ys]) :- X =< Y.
insert(X, [Y|Ys], [Y|Zs]) :- X > Y, insert(X, Ys, Zs).
 
query(insertion_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in functionality. Both codes implement the insertion sort algorithm in Prolog. The generated code uses slightly different variable names (e.g., 'Head' instead of 'H', 'Tail' instead of 'T') and renames 'insert_element' to 'insert', but the logic remains unchanged. The running results of both codes are identical, producing the same sorted list.
*/