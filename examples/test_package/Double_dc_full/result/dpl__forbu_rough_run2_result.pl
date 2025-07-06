bubblesort([], Acc, Acc).
bubblesort([X], Acc, [X|Acc]).
bubblesort(List, Acc, Sorted) :-
    bubble(List, NewList, Max),
    bubblesort(NewList, [Max|Acc], Sorted).
bubble([X, Y|Rest], [X|NewRest], Max) :-
    X =< Y,
    bubble([Y|Rest], NewRest, Max).
bubble([X, Y|Rest], [Y|NewRest], Max) :-
    X > Y,
    bubble([X|Rest], NewRest, Max).
bubble([X], [], X).
forth_sort(L, L2) :- bubblesort(L, [], L2).
query(forth_sort([3,1,2,5,7,12], X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code correctly implements a bubble sort algorithm, similar to the original code but with a different structure. It uses a more straightforward approach for comparing and swapping elements, eliminating the need for separate 'hole' and 'swap' predicates. The generated code is consistent with the original in functionality, producing the same sorted output for the given input. However, the original code's approach with 'hole' and 'swap' predicates is more modular, while the generated code combines these steps directly in the 'bubble' predicate. Both codes are valid and produce the correct result.
*/