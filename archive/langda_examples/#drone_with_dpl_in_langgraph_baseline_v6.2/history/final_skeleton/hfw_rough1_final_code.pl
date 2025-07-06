Here's the complete DeepProbLog code based on the given ruleset and requirements:

```prolog
% Neural network declarations
nn(net1, [X], Y, [0,1,2,3,4,5,6,7,8,9]) :: detect_number(X, Y).
nn(net2, [X], Y, [+,-,*,/]) :: detect_operator(X, Y).

% Helper predicate for detecting all elements in a list
detect_all([N], [N2]) :- detect_number(N, N2).
detect_all([N,O|T], [N2,O2|T2]) :- 
    detect_number(N, N2), 
    detect_operator(O, O2), 
    detect_all(T, T2).

% Floating point comparison predicate
almost_equal(X, Y) :- ground(Y), abs(X-Y) < 0.0001.
almost_equal(X, Y) :- var(Y), Y is float(X).

% Expression evaluation predicate
expression(Images, Result) :- 
    detect_all(Images, Symbols),
    parse(Symbols, Result).

% Documentation predicates
langda(NET:"It receives a list of symbols recognized by a neural network", LLM:"calculates them step by step according to mathematical rules, and outputs the value of the expression.").

% Parser for mathematical expressions
parse([N], N).
parse([N1, Op, N2 | T], Result) :-
    compute(Op, N1, N2, R),
    parse([R | T], Result).

% Computation rules
compute(+, A, B, R) :- R is A + B.
compute(-, A, B, R) :- R is A - B.
compute(*, A, B, R) :- R is A * B.
compute(/, A, B, R) :- R is A / B.
```

This code includes:
1. The neural network declarations for digit and operator recognition
2. The detect_all predicate for processing lists of images
3. The almost_equal helper predicate for floating point comparisons
4. The main expression evaluation predicate
5. The documentation predicate
6. The parse and compute predicates for evaluating mathematical expressions

The code follows all the requirements and avoids using the '->' symbol as requested. It maintains all the functionality described in the original ruleset.