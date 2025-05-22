% Insertion sort algorithm in ProbLog
insertion_sort(List, Sorted) :-
    i_sort(List, [], Sorted).

% Base case: when the input list is empty, the accumulator is the sorted list
i_sort([], Acc, Acc).

% Recursive case: insert the head of the list into the accumulator and continue
i_sort([H|T], Acc, Sorted) :-
    insert(H, Acc, NewAcc),
    i_sort(T, NewAcc, Sorted).

% Insert an element into a sorted list
insert(X, [], [X]).

insert(X, [Y|T], [X,Y|T]) :-
    X =< Y.

insert(X, [Y|T], [Y|NewT]) :-
    X > Y,
    insert(X, T, NewT).
 
query(insertion_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code correctly implements the insertion sort algorithm in ProbLog, similar to the original code. Both versions produce the same sorted output for the given input. The generated code uses an accumulator pattern, which is a common optimization in Prolog-style languages, making it slightly more efficient. The logic and functionality remain consistent with the original code. No problems were identified in the generated code.