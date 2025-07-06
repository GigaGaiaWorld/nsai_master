stack_op(sort, Stack, SortedStack) :- length(Stack, Len), (Len >= 3 -> get_top_n(Stack, 3, Elements, RestStack), insertion_sort(Elements, SortedElements), append(SortedElements, RestStack, SortedStack) ; SortedStack = Stack).
get_top_n(Stack, N, Elements, Rest) :- length(Elements, N), append(Elements, Rest, Stack).
insertion_sort(List, Sorted) :- insertion_sort(List, [], Sorted).
insertion_sort([], Acc, Acc).
insertion_sort([H | T], Acc, Sorted) :- insert(H, Acc, NewAcc), insertion_sort(T, NewAcc, Sorted).
insert(X, [], [X]).
insert(X, [Y | T], [X, Y | T]) :- X =< Y.
insert(X, [Y | T], [Y | NewT]) :- X > Y, insert(X, T, NewT).
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