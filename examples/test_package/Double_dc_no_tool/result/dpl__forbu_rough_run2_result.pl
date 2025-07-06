bubblesort([], Acc, Acc).
bubblesort([X], Acc, Sorted) :- 
    append(Acc, [X], Sorted).
bubblesort(List, Acc, Sorted) :-
    bubble_pass(List, NewList, Swapped),
    (Swapped == true ->
        bubblesort(NewList, Acc, Sorted)
    ;
        append(Acc, NewList, Sorted)
    ).

bubble_pass([X,Y|Rest], [Y|NewRest], true) :-
    X > Y,
    bubble_pass([X|Rest], NewRest, _).
bubble_pass([X,Y|Rest], [X|NewRest], Swapped) :-
    X =< Y,
    bubble_pass([Y|Rest], NewRest, Swapped).
bubble_pass([X], [X], false).
bubble_pass([], [], false).

forth_sort(L,L2) :- bubblesort(L,[],L2).

query(forth_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code attempts to implement a bubble sort algorithm but contains syntax errors and logical issues. The main problem is the incorrect use of the '->' operator in the bubblesort predicate, which causes a runtime error. The original code correctly implements bubble sort using a different approach with hole/4 and swap/3 predicates. The generated code's structure differs significantly from the original and fails to execute properly.
*/