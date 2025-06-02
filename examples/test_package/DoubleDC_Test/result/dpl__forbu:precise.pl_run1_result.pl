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
swap(X, Y, no_swap) :- X =< Y.
swap(X, Y, swap) :- X > Y.
 
query(forth_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is mostly consistent with the original code in terms of functionality and structure. The main difference lies in the 'swap' predicate, where the original uses '<' and '\+ swap(X,Y,no_swap)', while the generated code uses '=<' and '>'. This change does not affect the correctness of the sorting logic, as both versions correctly handle the comparison and swapping of elements. The running results of both codes are identical, producing the same sorted list. The generated code is valid and meets the requirements.
*/