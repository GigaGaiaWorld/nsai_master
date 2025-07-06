stack_op(sort(N), Stack, SortedStack) :- (length(Stack, Len), Len >= N -> get_top_n(Stack, N, Elements, RestStack), insertion_sort(Elements, SortedElements), append(SortedElements, RestStack, SortedStack) ; SortedStack = Stack).
get_top_n(Stack, N, Elements, Rest) :- length(Elements, N), append(Elements, Rest, Stack).
insertion_sort(List, Sorted) :- insertion_sort_aux(List, [], Sorted).
insertion_sort_aux([], Acc, Acc).
insertion_sort_aux([X|Xs], Acc, Sorted) :- insert(X, Acc, NewAcc), insertion_sort_aux(Xs, NewAcc, Sorted).
insert(X, [], [X]).
insert(X, [Y|Ys], [X, Y|Ys]) :- X =< Y.
insert(X, [Y|Ys], [Y|Zs]) :- X > Y, insert(X, Ys, Zs).
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
stack_op(push(1),[2, 3, 4],X2) = 0.0000
stack_op(pop,[1, 2, 3, 4],X2) = 0.0000
stack_op(dup,[1, 2, 3, 4],X2) = 0.0000
stack_op(swap,[1, 2, 3, 4],X2) = 0.0000
stack_op(over,[1, 2, 3, 4],X2) = 0.0000
stack_op(rot,[1, 2, 3, 4],X2) = 0.0000
*/