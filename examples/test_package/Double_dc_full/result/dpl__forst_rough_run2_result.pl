stack_op(push(X), Stack, [X|Stack]).
stack_op(pop, [X|Rest], Rest).
stack_op(dup, [X|Rest], [X,X|Rest]).
stack_op(swap, [X,Y|Rest], [Y,X|Rest]).
stack_op(over, [X,Y|Rest], [Y,X,Y|Rest]).
stack_op(rot, [X,Y,Z|Rest], [Z,X,Y|Rest]).
stack_op(sort, Stack, SortedStack) :-
    get_top_n(Stack, 3, Elements, RestStack),
    insertion_sort(Elements, SortedElements),
    append(SortedElements, RestStack, SortedStack).
get_top_n(Stack, N, Elements, Rest) :-
    length(Elements, N),
    append(Elements, Rest, Stack).
insertion_sort(List, Sorted) :-
    insertion_sort(List, [], Sorted).
insertion_sort([], Acc, Acc).
insertion_sort([H|T], Acc, Sorted) :-
    insert(H, Acc, NewAcc),
    insertion_sort(T, NewAcc, Sorted).
insert(X, [], [X]).
insert(X, [Y|Rest], [X,Y|Rest]) :-
    X =< Y.
insert(X, [Y|Rest], [Y|NewRest]) :-
    X > Y,
    insert(X, Rest, NewRest).
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
Validity_result: True
Report: The generated code is correct and consistent with the original code. It includes all the stack operations (push, pop, dup, swap, over, rot) and the sorting operation with the same logic. The generated code also correctly implements the insertion_sort and get_top_n predicates, which were implied in the original code but not explicitly shown. The running results of both codes are identical, confirming that the generated code meets the expectations.
*/