insertion_sort([], []).
insertion_sort([H|T], Sorted) :-
 

    insertion_sort(T, SortedTail),
    insert_element(H, SortedTail, Sorted).
insert_element(X, [], [X]).
insert_element(X, [H|T], [X,H|T]) :-
 X =< H.
insert_element(X, [H|T], [H|RT]) :-
 X > H,
 insert_element(X, T, RT).
 
query(insertion_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is functionally identical to the original code, producing the same sorted list for the given input. The only differences are minor formatting changes (whitespace and line breaks), which do not affect the logic or execution. Both codes correctly implement the insertion sort algorithm in Prolog.
*/