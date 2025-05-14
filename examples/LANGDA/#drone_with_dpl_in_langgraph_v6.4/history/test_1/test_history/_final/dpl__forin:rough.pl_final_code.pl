% Insertion sort in ProbLog

% Base case: empty list is already sorted
insertion_sort([], []).

% Recursive case: insert head into sorted tail
insertion_sort([H|T], Sorted) :-
    insertion_sort(T, SortedTail),
    insert(H, SortedTail, Sorted).

% Inserting into empty list
insert(X, [], [X]).

% Inserting into non-empty list
insert(X, [Y|Ys], [X,Y|Ys]) :-
    X =< Y.
insert(X, [Y|Ys], [Y|Zs]) :-
    X > Y,
    insert(X, Ys, Zs).

% Example query:
% query(insertion_sort([3,1,2,5,7,12],X))
.
 
query(insertion_sort([3,1,2,5,7,12],X)).

*** Result:*** 
Error evaluating Problog model:
    return list(map(f, l))
           ^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/parser.py", line 1013, in _extract_statements
    raise ParseError(string, "Empty statement found", token.location)
problog.parser.ParseError: Empty statement found at 23:1. 

***Report:***
Validity_form:False\Validity_result:False
The generated code is mostly consistent with the original code in terms of logic and structure, implementing insertion sort correctly. However, there is a syntax error in the generated code due to an extra period (.) after the comment line for the example query, which causes a parsing error. This makes the generated code invalid. The original code runs successfully and produces the correct sorted list, while the generated code fails to run due to the syntax error.