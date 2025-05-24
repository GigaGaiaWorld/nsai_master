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
The generated code is functionally identical to the original code, producing the same sorted list for the given input. The only difference is the variable name 'TSorted' in the original code is changed to 'SortedT' in the generated code, which does not affect the logic or outcome. Both codes correctly implement the insertion sort algorithm in Prolog.