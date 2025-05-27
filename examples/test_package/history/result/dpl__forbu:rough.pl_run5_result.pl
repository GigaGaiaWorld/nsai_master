swap(X, Y, Y, X) :- X > Y.
swap(X, Y, X, Y) :- X =< Y.

bubble([X], [], X).
bubble([H1, H2 | T], [X1 | T1], X) :-
    swap(H1, H2, X1, X2),
    bubble([X2 | T], T1, X).

bubblesort([], L, L).
bubblesort(L, L3, Sorted) :-
    bubble(L, L2, X),
    bubblesort(L2, [X | L3], Sorted).

forth_sort(L, L2) :- bubblesort(L, [], L2).

query(forth_sort([3, 1, 2, 5, 7, 12], X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and meets the requirements. It maintains the same functionality as the original code, implementing a bubble sort algorithm. The main difference is in the 'swap' predicate, which in the generated code directly swaps the elements if X > Y, whereas the original code uses a 'hole' predicate with a swap/no_swap flag. Despite this difference in implementation, the logic remains consistent, and the sorting behavior is identical. Both codes produce the same sorted output for the given input.
*/