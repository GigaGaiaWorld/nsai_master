insertion_sort(List, Sorted) :- 
    insertion_sort(List, [], Sorted).

insertion_sort([], Acc, Acc).
insertion_sort([H|T], Acc, Sorted) :-
    insert(H, Acc, NewAcc),
    insertion_sort(T, NewAcc, Sorted).

insert(X, [], [X]).
insert(X, [Y|Ys], [X,Y|Ys]) :-
    X =< Y.
insert(X, [Y|Ys], [Y|Zs]) :-
    X > Y,
    insert(X, Ys, Zs).
 
query(insertion_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code correctly implements the insertion sort algorithm, similar to the original code but using an accumulator for tail recursion optimization. Both versions produce the same sorted output for the given input. The generated code is valid and meets the requirements, with consistent results compared to the original code.
*/