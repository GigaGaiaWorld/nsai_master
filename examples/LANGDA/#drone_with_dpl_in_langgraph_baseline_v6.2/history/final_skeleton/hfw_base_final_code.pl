Here's the complete DeepProbLog code based on the given ruleset:

```prolog
% Neural network predicates for digit and operator recognition
nn(net1, [X], Y, [0,1,2,3,4,5,6,7,8,9]) :: detect_number(X, Y).
nn(net2, [X], Y, [+,-,*,/]) :: detect_operator(X, Y).

% Helper predicate for floating point comparison
almost_equal(X, Y) :- ground(Y), abs(X-Y) < 0.0001.
almost_equal(X, Y) :- var(Y), Y is float(X).

% Detect all symbols in the image sequence
detect_all([N], [N2]) :- detect_number(N, N2).
detect_all([N,O|T], [N2,O2|T2]) :- 
    detect_number(N, N2), 
    detect_operator(O, O2), 
    detect_all(T, T2).

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

% Division case (with zero check)
parse([N1,/,N2|T], R) :-
    N2 \== 0,
    N3 is N1/N2,
    parse([N3|T], R).
```

This code implements:
1. Two neural networks (net1 and net2) for recognizing digits and operators respectively
2. A helper predicate `almost_equal/2` for floating point comparison
3. The `detect_all/2` predicate that processes a sequence of images into symbols
4. The main `expression/2` predicate that ties everything together
5. The recursive `parse/2` predicate that evaluates mathematical expressions with:
   - Single number handling
   - Addition
   - Subtraction (implemented as addition of negative)
   - Multiplication
   - Division (with zero division check)

The code follows standard Prolog syntax and avoids using the '->' symbol as requested.