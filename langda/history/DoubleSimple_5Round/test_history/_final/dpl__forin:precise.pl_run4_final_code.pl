insertion_sort([], []).
insertion_sort([H|T], Sorted) :-
 

 insertion_sort(T, SortedT),
 insert_element(H, SortedT, Sorted).

insert_element(X, [], [X]).
insert_element(X, [H|T], [X,H|T]) :-
 X =< H.
insert_element(X, [H|T], [H|RT]) :-
 X > H,
 insert_element(X, T, RT).

query(insertion_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code. Both codes implement the insertion sort algorithm in Prolog, and they produce the same sorted output for the given input list [3,1,2,5,7,12]. The generated code maintains the same logic and structure as the original, with only minor formatting differences, such as spacing and line breaks, which do not affect the functionality.