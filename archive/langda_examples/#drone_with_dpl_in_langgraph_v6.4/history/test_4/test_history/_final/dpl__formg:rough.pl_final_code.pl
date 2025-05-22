% Merge Sort in ProbLog

% Base case for splitting a list into two halves
split([], [], []).
split([X], [X], []).
split([X,Y|Xs], [X|Left], [Y|Right]) :-
    split(Xs, Left, Right).

% Merge two sorted lists into one sorted list
merge([], Right, Right).
merge(Left, [], Left).
merge([X|Left], [Y|Right], [X|Merged]) :-
    X =< Y,
    merge(Left, [Y|Right], Merged).
merge([X|Left], [Y|Right], [Y|Merged]) :-
    X > Y,
    merge([X|Left], Right, Merged).

% Merge sort implementation
merge_sort([], []).
merge_sort([X], [X]).
merge_sort(List, Sorted) :-
    split(List, Left, Right),
    merge_sort(Left, SortedLeft),
    merge_sort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted)
.
append([], L, L).
append([H|T], L2, [H|R]) :-
 append(T, L2, R).
query(merge_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
merge_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code correctly implements the merge sort algorithm in ProbLog, similar to the original code. The main difference lies in the implementation of the 'split' function, which is more concise in the generated code. The generated code splits the list by alternating elements between the left and right sublists, whereas the original code splits the list into two halves based on length. Despite this difference, both implementations achieve the same result. The generated code is valid and meets the requirements, and the running results are consistent with the original code.