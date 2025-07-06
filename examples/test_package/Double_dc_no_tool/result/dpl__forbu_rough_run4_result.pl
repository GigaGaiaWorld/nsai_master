bubblesort([], Acc, Acc).
bubblesort(List, Acc, Sorted) :-
    bubble(List, NewList, Changed),
    (Changed == true ->
        bubblesort(NewList, Acc, Sorted)
    ;
        append(NewList, Acc, Sorted)
    ).

bubble([X,Y|T], [Y|NewT], true) :-
    X > Y,
    bubble([X|T], [X|NewT], _).
bubble([X,Y|T], [X|NewT], Changed) :-
    X =< Y,
    bubble([Y|T], NewT, Changed).
bubble([X], [X], false).
bubble([], [], false).

forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: False
Report: The generated code attempts to implement a bubble sort algorithm but differs significantly from the original code. The original code uses a 'hole' predicate to handle swaps and accumulates sorted elements in reverse order, while the generated code uses a 'Changed' flag to determine if further sorting is needed. The generated code is syntactically valid but fails to produce the correct sorted result, as evidenced by the 0.0000 probability in the run result. This indicates a logical error in the sorting implementation.
*/