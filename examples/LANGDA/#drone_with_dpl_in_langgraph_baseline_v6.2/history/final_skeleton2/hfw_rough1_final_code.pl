Here's the complete DeepProblog code that replaces the `langda` term while maintaining all the functionality:

```prolog
nn(net1,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: detect_number(X,Y).
nn(net2,[X],Y,[+,-,*,/]) :: detect_operator(X,Y).

detect_all([N],[N2]) :- detect_number(N,N2).
detect_all([N,O|T],[N2,O2|T2]) :- detect_number(N,N2), detect_operator(O,O2), detect_all(T,T2).

almost_equal(X,Y) :- ground(Y),abs(X-Y) < 0.0001.
almost_equal(X,Y) :- var(Y), Y is float(X).

expression(Images,Result) :- detect_all(Images,Symbols), parse(Symbols,Result).

parse([N], N).
parse([N1, Op, N2 | T], Result) :-
    evaluate(N1, Op, N2, Temp),
    parse([Temp | T], Result).

evaluate(N1, +, N2, Result) :- Result is N1 + N2.
evaluate(N1, -, N2, Result) :- Result is N1 - N2.
evaluate(N1, *, N2, Result) :- Result is N1 * N2.
evaluate(N1, /, N2, Result) :- Result is N1 / N2.
```

This code:
1. Keeps all the original neural network declarations and detection rules
2. Replaces the `langda` term with actual parsing and evaluation rules
3. Implements step-by-step calculation of mathematical expressions
4. Handles all four basic arithmetic operations
5. Maintains the same interface through the `expression/2` predicate
6. Processes expressions recursively to handle arbitrary length

The new code implements the functionality described in the natural language requirements without using the '->' symbol.