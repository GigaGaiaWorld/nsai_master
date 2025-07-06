bubblesort([], Acc, Acc).
bubblesort([X], Acc, [X|Acc]).
bubblesort([X, Y | Rest], Acc, Sorted) :-
    if_then_else(
        X > Y,
        bubblesort([X | Rest], [Y | Acc], Sorted),
        bubblesort([Y | Rest], [X | Acc], Sorted)
    ).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code attempts to implement a bubble sort algorithm but incorrectly uses 'if_then_else/3', which is not a built-in predicate in Prolog, leading to a runtime error. The original code correctly implements bubble sort using custom 'swap' and 'hole' predicates. The generated code's form is invalid due to the unrecognized predicate, and its result is inconsistent with the original code's successful execution.
*/