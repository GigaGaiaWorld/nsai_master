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
Report: The generated code correctly implements the insertion sort algorithm, similar to the original code. Both versions produce the same sorted output for the given input. The generated code uses an accumulator pattern, which is a different but valid approach compared to the original's recursive insertion. The logic for inserting elements is consistent between both versions, with minor syntactic differences. Both codes are valid and produce identical results.
*/