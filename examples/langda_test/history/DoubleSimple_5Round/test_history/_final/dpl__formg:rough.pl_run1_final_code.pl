append([], L, L).
append([H|T], L2, [H|R]) :-
    append(T, L2, R).

split(List, Left, Right) :-
    length(List, Len),
    Half is Len // 2,
    length(Left, Half),
    append(Left, Right, List).

merge([], Right, Right).
merge(Left, [], Left).
merge([L|Left], [R|Right], [L|Merged]) :-
    L =< R,
    merge(Left, [R|Right], Merged).
merge([L|Left], [R|Right], [R|Merged]) :-
    L > R,
    merge([L|Left], Right, Merged).

merge_sort([], []).
merge_sort([X], [X]).
merge_sort(List, Sorted) :-
    length(List, Len),
    Len > 1,
    split(List, Left, Right),
    merge_sort(Left, LeftSorted),
    merge_sort(Right, RightSorted),
    merge(LeftSorted, RightSorted, Sorted).

query(merge_sort([3,1,2,5,7,12],X)).
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in functionality. Both codes implement the merge sort algorithm in Prolog, including the helper predicates append, split (or split_list in the original), and merge. The generated code correctly sorts the list [3,1,2,5,7,12] into [1,2,3,5,7,12], matching the original code's output. The only difference is the renaming of 'split_list' to 'split' in the generated code, which does not affect the logic or outcome. The generated code is valid and meets the requirements.