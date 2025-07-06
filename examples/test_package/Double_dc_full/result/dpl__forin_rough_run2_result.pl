insertion_sort([], []).
insertion_sort([Head|Tail], Sorted) :-
    insertion_sort(Tail, SortedTail),
    insert(Head, SortedTail, Sorted).
insert(X, [], [X]).
insert(X, [Y|Tail], [X,Y|Tail]) :-
    X =< Y.
insert(X, [Y|Tail], [Y|SortedTail]) :-
    X > Y,
    insert(X, Tail, SortedTail).
 
query(insertion_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in functionality. Both codes implement the insertion sort algorithm in Prolog. The generated code uses slightly different variable names (e.g., 'Head' instead of 'H', 'Tail' instead of 'T') and renames the 'insert_element' predicate to 'insert', but the logic remains unchanged. The running results of both codes are identical, sorting the list [3,1,2,5,7,12] into [1,2,3,5,7,12] with a probability of 1.0000.
*/