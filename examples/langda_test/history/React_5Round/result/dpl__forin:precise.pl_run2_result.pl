insertion_sort([], []).
insertion_sort([H|T], Sorted) :-
 
insertion_sort(T, SortedT), insert_element(H, SortedT, Sorted).
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
Report: The generated code is functionally equivalent to the original code, producing the same correct sorted output for the given input. The only difference is a minor formatting issue where the second line of the insertion_sort predicate is split across two lines without proper indentation, which does not affect the code's execution or correctness.
*/