% Cryptoaddition:
% Find the unique answer to:
% Define available digits
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
% The first digit of a multi-digit number cannot be 0
leftdigit(D) :- digit(D), D =\= 0.
% All elements are different
all_different([]).
all_different([H|T]) :- \+ member(H, T), all_different(T).
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).
% Simulate a column addition: Cin is the input carry, Cout is the output carry
sumdigit(Cin, A, B, Sum, Cout) :-
 X is Cin + A + B,
 ( X < 10, Sum = X, Cout = 0
 ; 
 X >= 10, Sum is X - 10, Cout = 1 ).
% Main predicate: AB + BCD = CDE
query_sum([A,B,C,D,E]) :-
 
 leftdigit(A), leftdigit(B), leftdigit(C), AB is 10*A + B, BCD is 100*B + 10*C + D, CDE is 100*C + 10*D + E, AB + BCD =:= CDE, all_different([A,B,C,D,E]), sumdigit(0, B, D, E, Carry1), sumdigit(Carry1, A, C, D, Carry2), sumdigit(Carry2, 0, B, C, Carry3), Carry3 = 0.
% Initiate query example:
query(query_sum([A,B,C,D,E])).
/* %%% Result %%% 
Error evaluating Problog model:
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_builtin.py", line 887, in _builtin_is
    check_mode((a, b), ["*g"], functor="is", **k)
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_builtin.py", line 630, in check_mode
    raise CallModeError(functor, args, accepted, location=location)
problog.engine_builtin.CallModeError: Invalid argument types for call to 'is/2': arguments: (X1, 100*1+10*1+X2), expected: (any, ground) at 30:64.
*/