bubblesort([], Acc, Acc).
bubblesort(L, Acc, Sorted) :-
    bubble(L, NewL, Last),
    bubblesort(NewL, [Last | Acc], Sorted).

bubble([X], [], X).
bubble([H1, H2 | T], [X1 | T1], X) :-
    (H1 =< H2, X1 = H1, bubble([H2 | T], T1, X)) ;
    (H1 > H2, X1 = H2, bubble([H1 | T], T1, X)).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in terms of functionality. Both codes implement a bubble sort algorithm, and they produce the same sorted result for the given input. The generated code simplifies the original by removing the 'hole' and 'swap' predicates, directly embedding the comparison and swapping logic within the 'bubble' predicate. This makes the generated code more straightforward and easier to understand without altering the expected behavior.
*/