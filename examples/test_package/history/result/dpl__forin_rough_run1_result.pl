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
Report: The generated code correctly implements the insertion sort algorithm, similar to the original code. Both versions produce the same sorted output for the given input. The generated code uses an accumulator pattern, which is a common optimization in Prolog for tail recursion, making it slightly more efficient. The logic for inserting elements into the sorted list is consistent between both versions. No problems are identified in the generated code.
*/