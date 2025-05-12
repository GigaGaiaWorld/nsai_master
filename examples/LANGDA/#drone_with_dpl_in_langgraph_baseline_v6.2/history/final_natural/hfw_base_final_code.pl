Here's the complete DeepProblog code that replaces the langda terms while maintaining all the functionality from the original rule set:

```prolog
nn(net1,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: detect_number(X,Y).
nn(net2,[X],Y,[+,-,*,/]) :: detect_operator(X,Y).

detect_all([N],[N2]) :- detect_number(N,N2).
detect_all([N,O|T],[N2,O2|T2]) :- detect_number(N,N2), detect_operator(O,O2), detect_all(T,T2).

almost_equal(X,Y) :- ground(Y), abs(X-Y) < 0.0001.
almost_equal(X,Y) :- var(Y), Y is float(X).

expression(Images,Result) :- detect_all(Images,Symbols), parse(Symbols,Result).

parse([N],R) :- almost_equal(N,R).
parse([N1,+|T], R) :-
    parse(T,R2),
    almost_equal(N1+R2,R).
parse([N1,-|T], R) :-
    parse([-1,*|T],R2),
    almost_equal(N1+R2,R).
parse([N1,*,N2|T], R) :-
    N3 is N1*N2,
    parse([N3|T],R).
parse([N1,/,N2|T], R) :-
    N2 \== 0,
    N3 is N1/N2,
    parse([N3|T],R).
```

This code:
1. Maintains all the original neural network declarations (net1 and net2)
2. Preserves the detect_all predicate for processing sequences of numbers and operators
3. Includes the almost_equal predicate for numeric comparisons
4. Contains the expression predicate that ties everything together
5. Has the complete parse predicate with all the original arithmetic operations (addition, subtraction via multiplication by -1, multiplication, and division with zero check)

The code follows standard Prolog/ProbLog syntax and avoids using the '->' symbol as requested.