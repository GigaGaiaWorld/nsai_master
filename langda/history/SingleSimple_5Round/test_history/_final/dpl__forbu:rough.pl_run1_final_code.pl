bubblesort([], Acc, Acc).
bubblesort([H], Acc, Sorted) :- append(Acc, [H], Sorted).
bubblesort([H1,H2|T], Acc, Sorted) :-
    (H1 > H2 ->
        bubblesort([H2,H1|T], Acc, Sorted)
    ;
        append(Acc, [H1], NewAcc),
        bubblesort([H2|T], NewAcc, Sorted)
    ).

forth_sort(L,L2) :- bubblesort(L,[],L2).
query(forth_sort([3,1,2,5,7,12],X)).

*** Result:*** 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 4:14. 

***Report:***
Validity_form:False\Validity_result:False
The generated code attempts to implement a bubble sort but uses a different approach than the original code. The original code uses a helper predicate 'hole' and 'swap' to manage the swapping of elements, while the generated code tries to use conditional statements directly within the 'bubblesort' predicate. However, the generated code is invalid because it uses an unsupported operator '->' in Problog, leading to a runtime error. The original code correctly sorts the list, but the generated code fails to execute due to syntax issues.