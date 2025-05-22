Here's the complete DeepProblog code that captures all the requirements from the ruleset without using the '->' symbol:

```prolog
nn(net1,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: detect_number(X,Y).
nn(net2,[X],Y,[+,-,*,/]) :: detect_operator(X,Y).

detect_all([N],[N2]) :- detect_number(N,N2).
detect_all([N,O|T],[N2,O2|T2]) :- detect_number(N,N2), detect_operator(O,O2), detect_all(T,T2).

almost_equal(X,Y) :- ground(Y), abs(X-Y) < 0.0001.
almost_equal(X,Y) :- var(Y), Y is float(X).

parse([N],N).
parse([N1,O,N2|T],Result) :-
    calculate(N1,O,N2,Res),
    parse([Res|T],Result).

calculate(N1,+,N2,Res) :- Res is N1 + N2.
calculate(N1,-,N2,Res) :- Res is N1 - N2.
calculate(N1,*,N2,Res) :- Res is N1 * N2.
calculate(N1,/,N2,Res) :- Res is N1 / N2.

expression(Images,Result) :- 
    detect_all(Images,Symbols),
    parse(Symbols,Result).
```

This code:
1. Defines neural networks for number and operator detection
2. Implements detect_all to process a sequence of images
3. Includes the almost_equal predicate for floating point comparison
4. Provides parsing and calculation of mathematical expressions
5. Defines the main expression predicate that ties everything together

The code follows mathematical rules to evaluate expressions step by step and returns the final result.