% Cryptoaddition:
% Find the unique answer to:
% SEND
% + MORE
% -------
% MONEY
query_sum([C,R,O,S,S,R,O,A,D,S]) :-
 
% Cryptoaddition puzzle: CROSS + ROADS = DANGER
query_sum([C, R, O, S, S, R, O, A, D, S]) :-
    leftdigit(C),
    leftdigit(R),
    leftdigit(D),
    all_different([C, R, O, S, A, D, E, N, G]),
    S1 is S + S,
    S2 is S1 mod 10,
    Carry1 is S1 // 10,
    O1 is O + A + Carry1,
    O2 is O1 mod 10,
    Carry2 is O1 // 10,
    R1 is R + O + Carry2,
    R2 is R1 mod 10,
    Carry3 is R1 // 10,
    C1 is C + R + Carry3,
    C2 is C1 mod 10,
    Carry4 is C1 // 10,
    D is Carry4,
    S2 = E,
    O2 = N,
    R2 = G,
    C2 = D.
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
    rf = self.fold(
         ^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/parser.py", line 1101, in fold
    raise ParseError(
problog.parser.ParseError: Operator priority clash at 10:43.