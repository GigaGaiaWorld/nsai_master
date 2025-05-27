stack_op(push(X), Stack, [X | Stack]).
stack_op(pop, [X | Stack], Stack).
stack_op(dup, [X | Stack], [X, X | Stack]).
stack_op(swap, [X, Y | Stack], [Y, X | Stack]).
stack_op(over, [X, Y | Stack], [Y, X, Y | Stack]).
stack_op(rot, [X, Y, Z | Stack], [Y, Z, X | Stack]).
stack_op(sort, Stack, SortedStack) :-
    is_list(Stack),
    length(Stack, Len),
    Len >= 3,
    get_top_n(Stack, 3, Elements, RestStack),
    quick_sort(Elements, SortedElements),
    append(SortedElements, RestStack, SortedStack).

get_top_n(Stack, N, Elements, Rest) :-
    length(Elements, N),
    append(Elements, Rest, Stack).

quick_sort([], []).
quick_sort([Pivot | Tail], Sorted) :-
    partition(Tail, Pivot, Left, Right),
    quick_sort(Left, SortedLeft),
    quick_sort(Right, SortedRight),
    append(SortedLeft, [Pivot | SortedRight], Sorted).

partition([], _, [], []).
partition([X | Tail], Pivot, [X | Left], Right) :-
    X =< Pivot,
    partition(Tail, Pivot, Left, Right).
partition([X | Tail], Pivot, Left, [X | Right]) :-
    X > Pivot,
    partition(Tail, Pivot, Left, Right).
stack_op(sort, Stack, SortedStack) :-
 get_top_n(Stack, 3, Elements, RestStack),
 insertion_sort(Elements, SortedElements),
 append(SortedElements, RestStack, SortedStack).
get_top_n(Stack, N, Elements, Rest) :-
 length(Elements, N),
 append(Elements, Rest, Stack).
query(stack_op(push(1),[2,3,4],Y)).
query(stack_op(pop,[1,2,3,4],Y)).
query(stack_op(dup,[1,2,3,4],Y)).
query(stack_op(swap,[1,2,3,4],Y)).
query(stack_op(over,[1,2,3,4],Y)).
query(stack_op(rot,[1,2,3,4],Y)).
/* %%% Result %%% 
% Problog Inference Result：
stack_op(push(1),[2, 3, 4],[1, 2, 3, 4]) = 1.0000
stack_op(pop,[1, 2, 3, 4],[2, 3, 4]) = 1.0000
stack_op(dup,[1, 2, 3, 4],[1, 1, 2, 3, 4]) = 1.0000
stack_op(swap,[1, 2, 3, 4],[2, 1, 3, 4]) = 1.0000
stack_op(over,[1, 2, 3, 4],[2, 1, 2, 3, 4]) = 1.0000
stack_op(rot,[1, 2, 3, 4],[2, 3, 1, 4]) = 1.0000
*/