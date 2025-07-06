Here's the complete DeepProblog code based on the provided ruleset and requirements:

```prolog
% Neural predicate for swap decision
nn(swap_net, [X,Y], Z, [no_swap, swap]) :: swap(X,Y,Z).

% Base cases for hole/4 (element swapping)
hole(X, Y, X, Y) :-
    swap(X, Y, no_swap).

hole(X, Y, Y, X) :-
    swap(X, Y, swap).

% Base case for bubble/3 (single element list)
bubble([X], [], X).

% Recursive case for bubble/3 (comparing adjacent elements)
bubble([H1, H2|T], [X1|T1], X) :-
    nn(bubble_net, [H1, H2], [X1, X2], [no_swap, swap]),
    hole(H1, H2, X1, X2),
    bubble([X2|T], T1, X).

% Base case for bubblesort/3 (empty accumulator)
bubblesort([], L, L).

% Recursive case for bubblesort/3 (main sorting process)
bubblesort(L, L3, Sorted) :-
    bubble(L, L2, X),
    bubblesort(L2, [X|L3], Sorted).

% Wrapper predicate for bubblesort
forth_sort(L, L2) :-
    bubblesort(L, [], L2).
```

Key points about this implementation:
1. I've replaced `lann` with `nn` which is the standard DeepProblog syntax for neural predicates
2. The `bubble_net` neural network is added to handle the comparison and swapping decisions during the bubble pass
3. The recursive cases maintain the same logic as described in your natural language requirements
4. All predicates are properly connected to form the complete bubble sort algorithm
5. The code avoids using the '->' symbol as requested

The implementation follows the standard DeepProblog syntax while preserving all the functionality described in your ruleset. The neural networks (swap_net and bubble_net) will need to be properly defined and trained separately.