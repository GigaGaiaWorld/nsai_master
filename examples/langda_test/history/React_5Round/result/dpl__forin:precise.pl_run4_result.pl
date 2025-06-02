insertion_sort([], []).
insertion_sort([H|T], Sorted) :-
 
insertion_sort(T, SortedT), insert_element(H, SortedT, Sorted)
.
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
Report: The generated code is functionally equivalent to the original code. Both implement insertion sort correctly, with the same logic for sorting and inserting elements. The only differences are in formatting (whitespace and line breaks), which do not affect the code's execution or results. The generated code maintains the same predicates and clauses as the original, ensuring consistent behavior.
*/