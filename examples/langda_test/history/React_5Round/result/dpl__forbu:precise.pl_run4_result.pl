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
swap(X,Y,swap) :- X > Y.
swap(X,Y,no_swap) :- X =< Y.
 
query(forth_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: true
Validity_result: true
Report: The generated code is functionally equivalent to the original code, producing the same sorted result for the given input. The main difference lies in the 'swap' predicate definitions: the original uses negation ('\+ swap(X,Y,no_swap)') for the swap case, while the generated code explicitly defines 'swap(X,Y,swap)' as 'X > Y' and 'no_swap' as 'X =< Y'. Both implementations correctly handle the swapping logic for bubble sort. The generated code maintains the same structure and logic flow as the original.
*/