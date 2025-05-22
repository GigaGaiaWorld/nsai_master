% Insertion Sort in ProbLog

% Base case: an empty list is already sorted
insertion_sort([], []).

% Recursive case: insert the head into the sorted tail
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).

% Insert an element into a sorted list
insert(X, [], [X]).
insert(X, [Y|T], [X,Y|T]) :-
    X =< Y.
insert(X, [Y|T], [Y|SortedT]) :-
    X > Y,
    insert(X, T, SortedT)
.
 
query(insertion_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality. Both codes implement the insertion sort algorithm in Prolog, with identical logic for sorting and inserting elements. The only differences are in variable naming (e.g., 'insert_element' vs 'insert') and minor formatting, which do not affect the behavior. The running results of both codes are identical, producing the same sorted list with a probability of 1.0000.