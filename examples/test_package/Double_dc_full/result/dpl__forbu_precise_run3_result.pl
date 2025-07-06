hole(X,Y,X,Y):-
 swap(X,Y,no_swap).
hole(X,Y,Y,X):-
 swap(X,Y,swap).
bubble([X],[],X).
bubble([H1,H2|T],[X1|T1],X):-
 hole(H1,H2,X1,X2),
 bubble([X2|T],T1,X).
bubblesort([],L,L).
bubblesort(L,L3,Sorted) :-
 

    bubble(L, L2, X),
    bubblesort(L2, [X | L3], Sorted).
forth_sort(L,L2) :- bubblesort(L,[],L2).
swap(X, Y, swap) :-
    X > Y.
swap(X, Y, no_swap) :-
    X =< Y.
 
query(forth_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: true
Validity_result: true
Report: The generated code is correct and consistent with the original code in functionality. Both codes implement a bubble sort algorithm in Prolog, and they produce the same sorted output for the given input list [3,1,2,5,7,12]. The main difference lies in the definition of the swap/3 predicate: the original code uses negation as failure (\+ swap(X,Y,no_swap)) for the swap case, while the generated code explicitly checks X > Y for swap and X =< Y for no_swap. This change is logically equivalent and does not affect the outcome.
*/