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
Report: The generated code is correct and consistent with the original code in terms of functionality. Both codes implement the insertion sort algorithm in Prolog, and they produce the same sorted output for the given input list. The generated code uses an accumulator pattern, which is a common optimization in Prolog to make the recursion more efficient, while the original code does not. Despite this difference in implementation, the logic and results are identical.
*/