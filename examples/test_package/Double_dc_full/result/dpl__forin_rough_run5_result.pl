insertion_sort([], []).
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).
insert(X, [], [X]).
insert(X, [H|T], [X,H|T]) :-
    X =< H.
insert(X, [H|T], [H|SortedT]) :-
    X > H,
    insert(X, T, SortedT).
 
query(insertion_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in functionality. Both codes implement the insertion sort algorithm in Prolog. The only difference is the renaming of the predicate 'insert_element' to 'insert' in the generated code, which does not affect the logic or outcome. The running results of both codes are identical, producing the same sorted list.
*/