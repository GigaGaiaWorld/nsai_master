% Cryptoaddition:
% Find the unique answer to:
%   SEND
% + MORE
% -------
%  MONEY

query_sum([S,E,N,D,M,O,R,Y]) :-
    digit(D), digit(E), D=\=E,
    sumdigit(0, D, E, Y, C1),
    
    digit(N), all_different([N,Y,E,D]),
    
    digit(R), all_different([R,N,Y,E,D]),
    sumdigit(C1, N, R, E, C2),
    
    digit(O), all_different([O,R,N,Y,E,D]),
    sumdigit(C2, E, O, N, C3),
    
    leftdigit(S), all_different([S,O,R,N,Y,E,D]),
    leftdigit(M), all_different([M,S,O,R,N,Y,E,D]),
    sumdigit(C3, S, M, O, M),
    
    all_different([S,E,N,D,M,O,R,Y]).

sumdigit(C, A, B, S, 0) :-
    X is C + A + B,
    X < 10,
    S = X.

sumdigit(C, A, B, S, 1) :-
    X is C + A + B,
    X >= 10,
    S is X - 10.

digit(0). digit(1). digit(2). digit(3). digit(4).
digit(5). digit(6). digit(7). digit(8). digit(9).

leftdigit(D) :- digit(D), D =\= 0.

all_different([]).
all_different([H|T]) :- \+ member(H, T), all_different(T).

member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

query(query_sum(X)).