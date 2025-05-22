% DeepProbLog compatible interpretable bubblesort algorithm

% Main sorting predicate
bubblesort([], Acc, Acc).
bubblesort(L, Acc, Sorted) :-
    bubble_pass(L, L1, Changed),
    (Changed == true ->
        bubblesort(L1, Acc, Sorted)
    ;
        append(Acc, L1, Sorted)
    ).

% Single pass of bubble sort
bubble_pass([X,Y|T], [Y|Rest], true) :-
    X > Y,
    bubble_pass([X|T], Rest, _).
bubble_pass([X,Y|T], [X|Rest], Changed) :-
    X =< Y,
    bubble_pass([Y|T], Rest, Changed).
bubble_pass([X], [X], false).
bubble_pass([], [], false).

% Helper predicate for list concatenation
append([], L, L).
append([H|T], L, [H|R]) :- append(T, L, R).

% Wrapper predicate for DeepProbLog queries
forth_sort(L, L2) :- bubblesort(L, [], L2).

% Probabilistic facts (dummy example for DeepProbLog)
0.5::dummy.

% Query example for DeepProbLog
query(forth_sort([3,1,2,5,7,12], _))
.
forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).

*** Result:*** 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 7:22. 

***Report:***
Validity_form:False\Validity_result:False
The generated code attempts to implement a bubblesort algorithm compatible with DeepProbLog but contains several issues. The main problem is the use of an unsupported '->' operator in the bubblesort predicate, which causes the execution error. The original code successfully implements a working bubblesort, while the generated code fails to run due to syntax errors. The generated code also includes unnecessary elements like a dummy probabilistic fact that don't contribute to the sorting functionality.