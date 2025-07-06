% Cryptoaddition:
% Find the unique answer to:
%   SEND
% + MORE
% -------
%  MONEY

query_sum([C,R,O,S,S,R,O,A,D,S]) :-
    langda(LLM:"
        % Cryptoaddition:
        % Find the unique answer to:
        %   CROSS
        % + ROADS
        % -------
        %  DANGER
        ").

digit(0). digit(1). digit(2). digit(3). digit(4).
digit(5). digit(6). digit(7). digit(8). digit(9).

leftdigit(D) :- digit(D), D =\= 0.

all_different([]).
all_different([H|T]) :- \+ member(H, T), all_different(T).

member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

query(query_sum(X)).