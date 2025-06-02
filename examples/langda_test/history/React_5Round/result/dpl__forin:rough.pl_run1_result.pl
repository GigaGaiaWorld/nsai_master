% Deterministic base case
insertion_sort(List,Sorted) :- 
    is_list(List),
    insertion_sort(List,[],Sorted).

% Probabilistic version that could account for uncertainty in comparisons
0.99::insertion_sort([],Acc,Acc).
0.01::insertion_sort([],Acc,Acc) :- false.  % Small chance of failure

0.98::insertion_sort([H|T],Acc,Sorted) :-
    insert(H,Acc,NAcc),
    insertion_sort(T,NAcc,Sorted).
0.02::insertion_sort([H|T],Acc,Sorted) :- 
    \+ insert(H,Acc,_),  % Small chance of failing to insert
    insertion_sort([H|T],Acc,Sorted).

% Insert rules with probabilistic ordering
0.95::insert(X,[],[X]).
0.05::insert(X,[],[X]) :- false.

0.90::insert(X,[Y|T],[Y|NT]) :- X > Y, insert(X,T,NT).
0.10::insert(X,[Y|T],[Y|NT]) :- X =< Y.  % Chance of incorrect ordering

0.90::insert(X,[Y|T],[X,Y|T]) :- X =< Y.
0.10::insert(X,[Y|T],[X,Y|T]) :- X > Y.  % Chance of incorrect ordering

% Type checking
is_list([]).
is_list([_|T]) :- is_list(T).
 
query(insertion_sort([3,1,2,5,7,12],X)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code attempts to introduce probabilistic elements into the insertion sort algorithm, which is a significant deviation from the deterministic nature of the original code. However, it fails to execute due to an attempt to overwrite the built-in 'is_list/1' predicate, which is not allowed in Problog. This makes the generated code invalid. The original code correctly implements a deterministic insertion sort and produces the expected sorted list. The generated code's approach to probabilistic sorting is conceptually interesting but is not valid due to the implementation error.
*/