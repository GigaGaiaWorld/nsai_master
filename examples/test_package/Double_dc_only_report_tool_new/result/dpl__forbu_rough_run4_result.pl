bubblesort([], Acc, Acc).
bubblesort([X], Acc, Sorted) :- append([X], Acc, Sorted).
bubblesort([X, Y | Rest], Acc, Sorted) :-
    X =< Y,
    bubblesort([Y | Rest], [X | Acc], Sorted).
bubblesort([X, Y | Rest], Acc, Sorted) :-
    X > Y,
    bubblesort([X | Rest], [Y | Acc], Sorted).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code attempts to implement a bubble sort but fails due to the use of 'append/3' which is not defined in the Problog environment. The original code correctly implements a bubble sort using a different approach with 'hole' and 'swap' predicates. The generated code is not valid as it results in an error during execution, while the original code runs successfully and produces the correct sorted list.
*/