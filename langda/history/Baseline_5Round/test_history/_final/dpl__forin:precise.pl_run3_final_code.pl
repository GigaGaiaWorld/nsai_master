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
The generated code is correct and consistent with the original code. Both codes implement the insertion sort algorithm in Prolog, and the variable names (e.g., TSorted vs. SortedT) are functionally equivalent. The running results of both codes are identical, producing the same sorted list with a probability of 1.0000.