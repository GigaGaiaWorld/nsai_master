lann(swap_net:"network that deal with swap", [X,Y],Z,[no_swap, swap]) :: swap(X,Y,Z).

hole(X,Y,X,Y):-
    swap(X,Y,no_swap).

hole(X,Y,Y,X):-
    swap(X,Y,swap).

bubble([X],[],X).
bubble([H1,H2|T],[X1|T1],X):- langda(LLM:"Single pass traversal process of the bubble algorithm").
bubblesort([],L,L).

bubblesort(L,L3,Sorted) :-
    langda(LLM:"Main body of bubble sort.").
forth_sort(L,L2) :- bubblesort(L,[],L2).