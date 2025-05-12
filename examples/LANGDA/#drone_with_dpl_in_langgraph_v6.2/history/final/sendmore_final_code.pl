% Cryptoaddition:
% Find the unique answer to:
% SEND
% + MORE
% -------
% MONEY
query_sum([C,R,O,S,S,R,O,A,D,S]) :-
 
leftdigit(C), leftdigit(R), leftdigit(D),
    digit(O), digit(A), digit(S), digit(N), digit(G), digit(E),
    all_different([C,R,O,S,A,D,N,G,E]),
    S + S + 10*O + 10*R + 100*A + 100*S + 1000*R + 1000*O + 10000*C =
    E + 10*R + 100*G + 1000*N + 10000*A + 100000*D.
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