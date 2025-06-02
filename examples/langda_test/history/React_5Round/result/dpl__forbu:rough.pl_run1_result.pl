bubblesort([], Acc, Acc).
bubblesort([H|T], Acc, Sorted) :-
    bubble(H, T, NT, Max),
    bubblesort(NT, [Max|Acc], Sorted).

bubble(X, [], [], X).
bubble(X, [Y|T], [X|NT], Max) :-
    X =< Y,
    bubble(Y, T, NT, Max).
bubble(X, [Y|T], [Y|NT], Max) :-
    X > Y,
    bubble(X, T, NT, Max).
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code correctly implements a bubble sort algorithm, similar to the original code but with a different structure. The original code uses a 'hole' predicate to handle swaps, while the generated code directly compares and swaps elements within the 'bubble' predicate. Both codes produce the same sorted result for the given input, indicating functional consistency. The generated code is valid and meets the requirements, with a cleaner and more straightforward implementation.
*/