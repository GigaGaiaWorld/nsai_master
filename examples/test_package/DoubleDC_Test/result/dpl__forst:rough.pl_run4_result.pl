stack_op(push(X), Stack, [X | Stack]).
stack_op(pop, [X | Stack], Stack).
stack_op(dup, [X | Stack], [X, X | Stack]).
stack_op(swap, [X, Y | Stack], [Y, X | Stack]).
stack_op(over, [X, Y | Stack], [Y, X, Y | Stack]).
stack_op(rot, [X, Y, Z | Stack], [Y, Z, X | Stack]).
stack_op(sort, Stack, SortedStack) :-
    get_top_n(Stack, 3, Elements, RestStack),
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
Report: The generated code is mostly correct and consistent with the original code, but there is a critical error in the 'rot' operation. The original code correctly rotates the top three elements as [Z,X,Y|Stack], while the generated code incorrectly rotates them as [Y,Z,X|Stack]. This results in inconsistent run results for the 'rot' operation. The rest of the operations (push, pop, dup, swap, over) and the sorting logic are correctly implemented and produce consistent results.
*/