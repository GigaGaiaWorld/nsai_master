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
 
 bubble(L, L2, X), bubblesort(L2, [X | L3], Sorted).
forth_sort(L,L2) :- bubblesort(L,[],L2).
swap(X, Y, swap) :- X > Y. swap(X, Y, no_swap) :- X =< Y.
 
query(forth_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: true
Validity_result: true
Report: The generated code is functionally equivalent to the original code, producing the same sorted result for the given input. The main difference lies in the 'swap' predicate definition: the original uses negation as failure (\+) while the generated code explicitly defines both cases with inequalities. Both versions correctly implement a bubble sort algorithm. The generated code is valid and maintains the same logic flow as the original.
*/