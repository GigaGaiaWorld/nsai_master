insertion_sort(List,Sorted) :- insertion_sort(List,[],Sorted).

insertion_sort([],Acc,Acc).
insertion_sort([H|T],Acc,Sorted) :-
    insert(H,Acc,NAcc),
    insertion_sort(T,NAcc,Sorted).

insert(X,[],[X]).
insert(X,[Y|T],[Y|NT]) :- X > Y, insert(X,T,NT).
insert(X,[Y|T],[X,Y|T]) :- X =< Y.
 
query(insertion_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code correctly implements the insertion sort algorithm, similar to the original code but using an accumulator for tail recursion optimization. Both codes produce the same sorted list for the given input. The generated code is more efficient due to tail recursion but maintains the same logic and outcome as the original.
*/