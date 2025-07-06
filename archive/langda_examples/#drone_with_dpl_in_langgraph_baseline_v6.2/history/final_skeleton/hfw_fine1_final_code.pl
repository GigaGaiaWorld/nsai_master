Here's the complete DeepProbLog code based on the provided ruleset and requirements:

```prolog
% Neural network predicates
nn(net1, [X], Y, [0,1,2,3,4,5,6,7,8,9]) :: detect_number(X, Y).
nn(net2, [X], Y, [+,-,*,/]) :: detect_operator(X, Y).

% Detection predicates
detect_all([N], [N2]) :- detect_number(N, N2).
detect_all([N,O|T], [N2,O2|T2]) :- 
    detect_number(N, N2), 
    detect_operator(O, O2), 
    detect_all(T, T2).

% Almost equal predicate
almost_equal(X, Y) :-
    (ground(Y) -> 
        abs(X - Y) < 0.0001
    ; 
        Y is float(X)
    ).

% Expression parsing
expression(Images, Result) :- 
    detect_all(Images, Symbols),
    parse(Symbols, Result).

% Base case for single number
parse([N], R) :-
    almost_equal(N, R).

% Addition case
parse([N1,+|T], R) :-
    parse(T, R2),
    almost_equal(N1 + R2, R).

% Subtraction case (converted to addition with negative)
parse([N1,-|T], R) :-
    parse([-1,*|T], R2),
    almost_equal(N1 + R2, R).

% Multiplication case
parse([N1,*,N2|T], R) :-
    N3 is N1 * N2,
    parse([N3|T], R).

% Division case (with check for division by zero)
parse([N1,/,N2|T], R) :-
    N2 \== 0,
    N3 is N1 / N2,
    parse([N3|T], R).
```

Note: The code includes the `almost_equal/2` predicate as described in the requirements, handling both cases where Y is ground and where it's a variable. The parsing rules implement arithmetic expression evaluation with proper operator precedence handling.