insertion_sort([], []).
insertion_sort([H|T], Sorted) :-
 
insertion_sort(T, SortedTail),
    insert_element(H, SortedTail, Sorted)
.
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
The generated code is functionally equivalent to the original code, producing the same correct sorting result. The only differences are in formatting (line breaks and spacing), which do not affect the logic or execution. The generated code maintains all the key components: the base case for empty list, recursive sorting, and proper element insertion logic. Both versions correctly implement insertion sort in Prolog.