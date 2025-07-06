insertion_sort(List, Sorted) :- insertion_sort(List, [], Sorted).

insertion_sort([], Sorted, Sorted).
insertion_sort([H|T], Acc, Sorted) :- insert(H, Acc, NewAcc), insertion_sort(T, NewAcc, Sorted).

insert(X, [], [X]).
insert(X, [Y|T], [X,Y|T]) :- X =< Y.
insert(X, [Y|T], [Y|NewT]) :- X > Y, insert(X, T, NewT).
 
query(insertion_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code correctly implements the insertion sort algorithm, similar to the original code but uses an accumulator for tail recursion optimization. Both codes produce the same sorted list for the given input, demonstrating functional consistency. The generated code is valid and meets the requirements, with no apparent issues.
*/