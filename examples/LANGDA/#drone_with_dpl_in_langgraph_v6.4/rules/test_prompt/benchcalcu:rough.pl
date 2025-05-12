% Cryptoaddition:
% Find the unique answer to:

query_sum([S,E,N,D,M,O,R,Y]) :-
    langda(LLM:"
        % Find the unique answer to:
        %   CROSS
        % + ROADS
        % -------
        %  DANGER
        ").

langda(LLM:"additional rules to complete query_sum/1").

digit(0). digit(1). digit(2). digit(3). digit(4).
digit(5). digit(6). digit(7). digit(8). digit(9).

leftdigit(D) :- digit(D), D =\= 0.

all_different([]).
all_different([H|T]) :- \+ member(H, T), all_different(T).

member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

query(query_sum(X)).