% Cryptoaddition:
% Find the unique answer to:
% SEND
% + MORE
% -------
% MONEY
query_sum([C,R,O,S,S,R,O,A,D,S]) :-
 
% Cryptoaddition:
% Find the unique answer to:
% CROSS
% + ROADS
% -------
% DANGER
query_sum([C,R,O,S,A,D,G,N,E]) :-
    leftdigit(C), leftdigit(R), leftdigit(D),
    digit(O), digit(A), digit(S), digit(G), digit(N), digit(E),
    % First column (rightmost)
    Sum1 is S + S,
    (Sum1 >= 10 -> Carry1 = 1 ; Carry1 = 0),
    E is Sum1 mod 10,
    % Second column
    Sum2 is O + A + Carry1,
    (Sum2 >= 10 -> Carry2 = 1 ; Carry2 = 0),
    G is Sum2 mod 10,
    % Third column
    Sum3 is S + D + Carry2,
    (Sum3 >= 10 -> Carry3 = 1 ; Carry3 = 0),
    N is Sum3 mod 10,
    % Fourth column
    Sum4 is R + O + Carry3,
    (Sum4 >= 10 -> Carry4 = 1 ; Carry4 = 0),
    A is Sum4 mod 10,
    % Fifth column
    Sum5 is C + R + Carry4,
    (Sum5 >= 10 -> Carry5 = 1 ; Carry5 = 0),
    D is Sum5 mod 10,
    Carry5 = 0,
    all_different([C,R,O,S,A,D,G,N,E]).
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
problog.parser.ParseError: Operator priority clash at 15:32.