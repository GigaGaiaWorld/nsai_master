% Merge Sort in Problog

% Base case: empty list or single element list is already sorted
merge_sort([], []).
merge_sort([X], [X]).

% Recursive case: split the list into two halves, sort each, and merge the results
merge_sort(List, Sorted) :-
    length(List, Len),
    Len > 1,
    Half is Len // 2,
    split(List, Half, Left, Right),
    merge_sort(Left, SortedLeft),
    merge_sort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).

% Split a list into two halves
split(List, Half, Left, Right) :-
    length(Left, Half),
    append(Left, Right, List).

% Merge two sorted lists into one sorted list
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
The generated code is correct and consistent with the original code. It implements the merge sort algorithm in Problog with the same logic and structure. The only minor difference is the renaming of 'split_list' to 'split', which does not affect functionality. Both codes produce the same correct result for the given query.