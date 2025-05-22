% Cryptoaddition:
% Find the unique answer to:
% SEND
% + MORE
% -------
% MONEY
query_sum([C,R,O,S,S,R,O,A,D,S]) :-
 
leftdigit(C), leftdigit(R), leftdigit(D),
    digit(O), digit(A), digit(S), digit(E), digit(N), digit(G),
    C1 is 0, C2 is 0, C3 is 0, C4 is 0, C5 is 0,
    S + S #= R + 10 * C1,
    R + R + C1 #= O + 10 * C2,
    O + A + C2 #= S + 10 * C3,
    S + D + C3 #= E + 10 * C4,
    C + R + C4 #= N + 10 * C5,
    D #= C5,
    all_different([C, R, O, S, A, D, E, N, G]).
a
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