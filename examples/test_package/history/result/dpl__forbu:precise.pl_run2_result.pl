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
swap(X, Y, swap) :- X > Y.
swap(X, Y, no_swap) :- X =< Y.
 
query(forth_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: true
Validity_result: true
Report: The generated code is correct and consistent with the original code in terms of functionality. Both codes implement a bubble sort algorithm in Prolog. The main difference lies in the definition of the 'swap' predicate. The original code uses negation ('\+ swap(X,Y,no_swap)') for the swap case, while the generated code directly defines the conditions ('X > Y' for swap and 'X =< Y' for no_swap). This change does not affect the correctness or the outcome of the sorting algorithm. The running results of both codes are identical, producing the same sorted list.
*/