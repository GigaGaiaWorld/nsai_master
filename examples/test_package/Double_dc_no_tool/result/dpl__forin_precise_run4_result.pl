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
Report: The generated code is functionally equivalent to the original code, producing the same correct sorted output for the given input. The logic of insertion sort is preserved, with identical predicate definitions and variable names. The only differences are minor formatting changes (extra whitespace and line breaks), which do not affect the code's execution or logic. Both codes correctly implement the insertion sort algorithm in Prolog.
*/