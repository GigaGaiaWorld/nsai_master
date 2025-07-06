merge_sort([], []).
merge_sort([X], [X]).

merge_sort(List, Sorted) :-
    length(List, Len),
    Len > 1,
    Half is Len // 2,
    split(List, Half, Left, Right),
    merge_sort(Left, SortedLeft),
    merge_sort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).

split([], _, [], []).
split([X|Xs], N, [X|Left], Right) :-
    N > 0,
    N1 is N - 1,
    split(Xs, N1, Left, Right).
split(List, _, [], List).

merge([], Right, Right).
merge(Left, [], Left).
merge([X|Left], [Y|Right], [X|Merged]) :-
    X =< Y,
    merge(Left, [Y|Right], Merged).
merge([X|Left], [Y|Right], [Y|Merged]) :-
    X > Y,
    merge([X|Left], Right, Merged).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality. Both codes implement the merge sort algorithm and produce the same sorted output for the given input. The generated code simplifies the split_list predicate into a split predicate, which is more efficient and concise. The merge and append predicates remain functionally identical. The generated code is valid and meets the requirements.