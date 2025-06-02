% Insertion sort implementation in Problog
insertion_sort(List, Sorted) :-
    insertion_sort_aux(List, [], Sorted).

% Base case: when input list is empty, return accumulated sorted list
insertion_sort_aux([], Acc, Acc).

% Recursive case: insert head into sorted position in accumulator
insertion_sort_aux([H|T], Acc, Sorted) :-
    insert(H, Acc, NewAcc),
    insertion_sort_aux(T, NewAcc, Sorted).

% Insert an element into a sorted list
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
Report: The generated code correctly implements insertion sort in Problog, similar to the original code but using an accumulator for tail recursion. Both versions produce the same sorted output for the given input. The generated code is more efficient due to tail recursion optimization. No functional differences or problems were found between the two implementations.
*/