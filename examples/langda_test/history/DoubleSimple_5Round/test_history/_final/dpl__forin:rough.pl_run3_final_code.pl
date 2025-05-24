insertion_sort(List,Sorted) :- insertion_sort(List,[],Sorted).

insertion_sort([],Acc,Acc).
insertion_sort([H|T],Acc,Sorted) :- insert(H,Acc,NAcc), insertion_sort(T,NAcc,Sorted).

insert(X,[],[X]).
insert(X,[Y|T],[Y|NT]) :- X > Y, insert(X,T,NT).
insert(X,[Y|T],[X,Y|T]) :- X =< Y.
 
query(insertion_sort([3,1,2,5,7,12],X)).

*** Result:*** 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code correctly implements the insertion sort algorithm, similar to the original code but uses an accumulator for tail recursion optimization. Both codes produce the same sorted output for the given input. The generated code is valid and meets the requirements, with consistent results.