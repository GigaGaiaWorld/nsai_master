Here's the complete Problog code with the `langda` term replaced by the supplementary logic for quicksort:

```prolog
nn(swap_net, [X,Y],Z,[no_swap, swap]) :: swap(X,Y,Z).

quicksort([X|Xs],Ys) :-
    partition(Xs,X,Left,Right),
    quicksort(Left,SortedLeft),
    quicksort(Right,SortedRight),
    append(SortedLeft,[X|SortedRight],Ys).
quicksort([],[]).

partition([X|Xs],Y,[X|Ls],Rs) :-
    swap(X,Y,swap), partition(Xs,Y,Ls,Rs).
partition([X|Xs],Y,Ls,[X|Rs]) :-
    swap(X,Y,no_swap), partition(Xs,Y,Ls,Rs).
partition([],Y,[],[]).

append([],Ys,Ys).
append([X|Xs],Ys,[X|Zs]) :- append(Xs,Ys,Zs).

forth_sort(L,L2) :- quicksort(L,L2).
```

The supplementary logic for quicksort:
1. Takes the pivot element X and partitions the list Xs into Left (elements less than X) and Right (elements greater than X)
2. Recursively sorts the Left and Right partitions
3. Combines the sorted Left partition, the pivot, and the sorted Right partition to form the final sorted list Ys