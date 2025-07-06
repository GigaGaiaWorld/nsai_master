bubblesort([], Acc, Acc).
bubblesort([X], Acc, [X|Acc]).
bubblesort([X,Y|Rest], Acc, Sorted) :-
    (X > Y,
     bubblesort([X|Rest], [Y|Acc], Sorted))
    ;
    (X =< Y,
     bubblesort([Y|Rest], [X|Acc], Sorted)).

forth_sort(L, L2) :- bubblesort(L, [], L2).

query(forth_sort([3,1,2,5,7,12], X)).

/* Result Report:
Validity_form: True
Validity_result: False
Report: The generated code is valid and correctly implements a sorting algorithm, but it sorts the list in descending order, whereas the original code sorts in ascending order. The generated code uses a direct comparison approach within the bubblesort predicate, which is simpler but produces different results. The original code uses a swap mechanism to ensure ascending order. Both codes are syntactically correct and meet their respective requirements, but they do not produce consistent results.
*/