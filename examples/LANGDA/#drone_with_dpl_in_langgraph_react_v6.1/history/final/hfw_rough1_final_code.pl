nn(net1,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: detect_number(X,Y).
nn(net2,[X],Y,[+,-,*,/]) :: detect_operator(X,Y).
detect_all([N],[N2]) :- detect_number(N,N2).
detect_all([N,O|T],[N2,O2|T2]) :- detect_number(N,N2), detect_operator(O,O2), detect_all(T,T2).
almost_equal(X,Y) :- ground(Y),abs(X-Y) < 0.
0001.
almost_equal(X,Y) :- var(Y), Y is float(X).
expression(Images,Result) :- detect_all(Images,Symbols),parse(Symbols,Result).
parse([N], N) :- number(N).
parse([N1, O, N2 | T], Result) :-
    number(N1),
    number(N2),
    calculate(O, N1, N2, R),
    parse([R | T], Result).

calculate(+, A, B, R) :- R is A + B.
calculate(-, A, B, R) :- R is A - B.
calculate(*, A, B, R) :- R is A * B.
calculate(/, A, B, R) :- R is A / B.