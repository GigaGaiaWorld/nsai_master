stack_op(push(X), Stack, [X | Stack]).
stack_op(pop, [X | Rest], Rest).
stack_op(dup, [X | Rest], [X, X | Rest]).
stack_op(swap, [X, Y | Rest], [Y, X | Rest]).
stack_op(over, [X, Y | Rest], [Y, X, Y | Rest]).
stack_op(rot, [X, Y, Z | Rest], [Y, Z, X | Rest]).
stack_op(sort(N), Stack, SortedStack) :-
    get_top_n(Stack, N, Elements, RestStack),
    insertion_sort(Elements, SortedElements),
    append(SortedElements, RestStack, SortedStack).

get_top_n(Stack, N, Elements, Rest) :-
    length(Elements, N),
    append(Elements, Rest, Stack).

insertion_sort(List, Sorted) :-
    insertion_sort_aux(List, [], Sorted).

insertion_sort_aux([], Acc, Acc).
insertion_sort_aux([H | T], Acc, Sorted) :-
    insert(H, Acc, NewAcc),
    insertion_sort_aux(T, NewAcc, Sorted).

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

/* Result Report:
Validity_form: True
Validity_result: False
Report: The generated code is mostly correct and consistent with the original code, with a few notable differences. The 'rot' operation in the generated code produces a different result ([2,3,1,4]) compared to the original ([3,1,2,4]), indicating an error in the implementation. The sorting operation is duplicated in the generated code, which is redundant but not functionally incorrect. The insertion sort implementation is correctly added and works as expected.
*/