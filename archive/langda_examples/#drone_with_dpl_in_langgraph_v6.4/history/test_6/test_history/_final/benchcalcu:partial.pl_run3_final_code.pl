% Cryptoaddition:
% Find the unique answer to:
query_sum([S,E,N,D,M,O,R,Y]) :-
 digit(D), digit(E), D=\=E,
 sumdigit(0, D, E, Y, C1),
 
 digit(N), all_different([N,Y,E,D]),
 
 digit(R), all_different([R,N,Y,E,D]),
 sumdigit(C1, N, R, E, C2),
 
 
digit(O), all_different([O,R,N,Y,E,D]),
sumdigit(C2, E, O, N, C3),

digit(M), all_different([M,O,R,N,Y,E,D]),
sumdigit(C3, S, M, O, C4),

leftdigit(S), leftdigit(M),
all_different([S,E,N,D,M,O,R,Y]),
% Ensure the sum of SEND and MORE equals MONEY
sumdigit(0, D, E, Y, C1),
sumdigit(C1, N, R, E, C2),
sumdigit(C2, E, O, N, C3),
sumdigit(C3, S, M, O, C4),
sumdigit(C4, 0, 0, 0, _).
 
 all_different([S,E,N,D,M,O,R,Y]).
sumdigit(C, A, B, S, 0) :-
 X is C + A + B,
 X < 10,
 S = X.
sumdigit(C, A, B, S, 1) :-
 X is C + A + B,
 X >= 10,
 S is X - 10.
digit(0).
 digit(1).
 digit(2).
 digit(3).
 digit(4).
digit(5).
 digit(6).
 digit(7).
 digit(8).
 digit(9).
leftdigit(D) :- digit(D), D =\= 0.
all_different([]).
all_different([H|T]) :- \+ member(H, T), all_different(T).
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).
query(query_sum(X)).

*** Result:*** 
Error evaluating Problog model:
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_builtin.py", line 887, in _builtin_is
    check_mode((a, b), ["*g"], functor="is", **k)
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_builtin.py", line 630, in check_mode
    raise CallModeError(functor, args, accepted, location=location)
problog.engine_builtin.CallModeError: Invalid argument types for call to 'is/2': arguments: (X1, 0+X2+0), expected: (any, ground) at 30:4. 

***Report:***
Validity_form:False\Validity_result:False
The generated code has several issues. First, it introduces an unnecessary variable C4 and incorrectly reuses sumdigit predicates, leading to redundancy. Second, the final sumdigit call with arguments (C4, 0, 0, 0, _) is invalid and causes a runtime error due to incorrect argument types. The original code correctly solves the cryptarithmetic problem, while the generated code fails to execute properly.