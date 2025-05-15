bubblesort([], Acc, Acc).

bubblesort([H1, H2 | T], Acc, Sorted) :-
    (H1 > H2 ->
        bubblesort([H2, H1 | T], Acc, Sorted)
    ;
        bubblesort([H1 | T], [H2 | Acc], Sorted)
    ).

forth_sort(L, L2) :- bubblesort(L, [], L2).

query(forth_sort([3,1,2,5,7,12], X)).

*** Result:*** 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 4:14. 

***Report:***
Validity_form:False\Validity_result:False
The generated code attempts to implement a bubble sort algorithm but contains syntax errors. The use of '->' operator is incorrect in this context, leading to a runtime error. The original code correctly implements bubble sort using helper predicates 'hole' and 'swap', while the generated code fails to execute due to improper Prolog syntax. The generated code does not meet expectations as it is not valid Prolog code.