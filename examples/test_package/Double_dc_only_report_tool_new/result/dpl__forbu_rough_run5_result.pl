bubblesort([], Acc, Acc).
bubblesort(L, Acc, Sorted) :-
    bubble(L, L1),
    (L = L1 ->
        append(Acc, L, Sorted)
    ;
        append(Acc, [H|T], NewAcc),
        bubblesort(L1, NewAcc, Sorted)
    ).
bubble([X, Y | T], [Y, X | T]) :- X > Y.
bubble([X | T], [X | T1]) :- bubble(T, T1).
forth_sort(L, L2) :- bubblesort(L, [], L2).
query(forth_sort([3,1,2,5,7,12], X)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code is not valid due to syntax errors in the conditional statement (->/2) which Problog cannot interpret. The original code uses a different approach with swap predicates and accumulates sorted elements differently. The generated code attempts to use a more imperative style with conditionals and append operations, which doesn't match Problog's logic programming paradigm. The running results are inconsistent as the generated code fails to execute at all.
*/