Here's the complete DeepProbLog code based on the given ruleset:

```prolog
% Neural network declarations
nn(net1, [X], Y, [0,1,2,3,4,5,6,7,8,9]) :: detect_number(X, Y).
nn(net2, [X], Y, [+,-,*,/]) :: detect_operator(X, Y).

% Detection of all symbols in the input
detect_all([N], [N2]) :- detect_number(N, N2).
detect_all([N,O|T], [N2,O2|T2]) :- 
    detect_number(N, N2), 
    detect_operator(O, O2), 
    detect_all(T, T2).

% Helper predicate for floating point comparison
almost_equal(X, Y) :- ground(Y), abs(X-Y) < 0.0001.
almost_equal(X, Y) :- var(Y), Y is float(X).

% Main expression evaluation predicate
expression(Images, Result) :- 
    detect_all(Images, Symbols),
    parse(Symbols, Result).

% Base case for parsing - single number
parse([N], R) :- almost_equal(N, R).

% Addition case
parse([N1,+|T], R) :-
    parse(T, R2),
    almost_equal(N1+R2, R).

% Subtraction case (converted to addition with negative)
parse([N1,-|T], R) :-
    parse([-1,*|T], R2),
    almost_equal(N1+R2, R).

% Multiplication case
parse([N1,*,N2|T], R) :-
    N3 is N1*N2,
    parse([N3|T], R).

% Division case (with check for division by zero)
parse([N1,/,N2|T], R) :-
    N2 \== 0,
    N3 is N1/N2,
    parse([N3|T], R).
```

This code implements:
1. Two neural networks (net1 for digit recognition, net2 for operator recognition)
2. A recursive symbol detection system that processes lists of images
3. An expression parser that handles:
   - Single numbers
   - Addition
   - Subtraction (implemented as addition of a negative)
   - Multiplication
   - Division (with protection against division by zero)
4. Floating point comparison with a small epsilon tolerance

The code follows all the requirements from the original ruleset and doesn't use the '->' symbol.