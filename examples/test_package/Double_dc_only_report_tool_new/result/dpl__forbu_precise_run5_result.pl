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
 
 bubble(L,L2,X), bubblesort(L2,[X|L3],Sorted).
forth_sort(L,L2) :- bubblesort(L,[],L2).
swap(X,Y,swap) :- X > Y. swap(X,Y,no_swap) :- X =< Y.
 
query(forth_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is functionally equivalent to the original code, producing the same sorted output for the given input. The main difference lies in the implementation of the swap/3 predicate, where the generated code uses 'X > Y' and 'X =< Y' conditions instead of the original 'X < Y' and '\+ swap(X,Y,no_swap)'. This change is logically equivalent and does not affect the outcome. Both codes correctly implement a bubble sort algorithm.
*/