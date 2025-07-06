insertion_sort([], []).
insertion_sort([H|T], Sorted) :-
 

    insertion_sort(T, SortedTail),
    insert_element(H, SortedTail, Sorted).

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
The generated code is correct and consistent with the original code. Both codes implement the insertion sort algorithm in Prolog and produce the same sorted output for the given query. The only difference is a minor formatting issue in the generated code where there is an extra line break and indentation, which does not affect the functionality or the result.