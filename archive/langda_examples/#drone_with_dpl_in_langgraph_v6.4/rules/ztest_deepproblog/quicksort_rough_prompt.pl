nn(swap_net, [X,Y],Z,[no_swap, swap]) :: swap(X,Y,Z).

quicksort([X|Xs],Ys) :-
  langda(LLM:"Supplementary logic of quicksort/2").
quicksort([],[]).

partition([X|Xs],Y,[X|Ls],Rs) :-
  swap(X,Y,swap), partition(Xs,Y,Ls,Rs).
partition([X|Xs],Y,Ls,[X|Rs]) :-
  swap(X,Y,no_swap), partition(Xs,Y,Ls,Rs).

partition([],Y,[],[]).

append([],Ys,Ys).
append([X|Xs],Ys,[X|Zs]) :- append(Xs,Ys,Zs).

forth_sort(L,L2) :- quicksort(L,L2).