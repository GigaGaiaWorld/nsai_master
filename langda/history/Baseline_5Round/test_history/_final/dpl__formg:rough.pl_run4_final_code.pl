% Base case: empty list is already sorted
merge_sort([], []).

% Base case: single element list is already sorted
merge_sort([X], [X]).

% Recursive case: split, sort halves, then merge
merge_sort(List, Sorted) :-
    length(List, Len),
    Len > 1,
    split(List, Left, Right),
    merge_sort(Left, SortedLeft),
    merge_sort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).

% Split list into two halves
split(List, Left, Right) :-
    length(List, Len),
    Half is Len // 2,
    length(Left, Half),
    append(Left, Right, List).

% Merge two sorted lists
merge([], Right, Right).
merge(Left, [], Left).
merge([L|Ls], [R|Rs], [L|Rest]) :-
    L =< R,
    merge(Ls, [R|Rs], Rest).
merge([L|Ls], [R|Rs], [R|Rest]) :-
    L > R,
    merge([L|Ls], Rs, Rest).

% Helper predicate for appending lists
append([], L, L).
append([H|T], L2, [H|R]) :-
    append(T, L2, R).

% Query example
query(merge_sort([3,1,2,5,7,12],X)).




*** Result:*** 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code. It maintains the same functionality for merge sort, including the base cases, recursive splitting, and merging of lists. The only difference is the renaming of 'split_list' to 'split', which does not affect the logic or outcome. The generated code produces the same sorted list as the original when queried with the same input.