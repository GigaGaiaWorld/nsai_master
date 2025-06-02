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
Report: The generated code is functionally equivalent to the original code. Both implement insertion sort correctly, with the same logic for sorting and inserting elements. The only differences are minor formatting changes (whitespace and line breaks), which do not affect the code's functionality. The running results of both codes are identical, producing the correct sorted list [1, 2, 3, 5, 7, 12] for the input [3, 1, 2, 5, 7, 12].
*/