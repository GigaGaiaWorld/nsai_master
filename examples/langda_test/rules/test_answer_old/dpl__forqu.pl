swap(X,Y,no_swap) :- X >= Y.
swap(X,Y,swap) :- \+ swap(X,Y,no_swap).

quicksort([X|Xs],Ys) :-
  partition(Xs,X,Left,Right),
  quicksort(Left,Ls),
  quicksort(Right,Rs),
  append(Ls,[X|Rs],Ys).
quicksort([],[]).

partition([X|Xs],Y,[X|Ls],Rs) :-
  swap(X,Y,swap), partition(Xs,Y,Ls,Rs).
partition([X|Xs],Y,Ls,[X|Rs]) :-
  swap(X,Y,no_swap), partition(Xs,Y,Ls,Rs).

partition([],Y,[],[]).

append([],Ys,Ys).
append([X|Xs],Ys,[X|Zs]) :- append(Xs,Ys,Zs).

forth_sort(L,L2) :- quicksort(L,L2).

query(forth_sort([3,1,2,5,7,12],X)).