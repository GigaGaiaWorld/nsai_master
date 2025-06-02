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
Report: The generated code is functionally correct and produces the same result as the original code. The logic for insertion sort is preserved, including the base case and recursive case for both insertion_sort and insert_element predicates. The only difference is a minor formatting issue where the line break after ':-' in the second clause of insertion_sort is unnecessary but does not affect the code's functionality.
*/