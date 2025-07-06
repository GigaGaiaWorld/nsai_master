detect_number(image_0, 0).
detect_number(image_1, 1).
detect_number(image_2, 2).
detect_number(image_3, 3).
detect_number(image_4, 4).
detect_number(image_5, 5).
detect_number(image_6, 6).
detect_number(image_7, 7).
detect_number(image_8, 8).
detect_number(image_9, 9).
detect_operator(image_plus, +).
detect_operator(image_minus, -).
detect_operator(image_multiply, *).
detect_operator(image_divide, /).
detect_all([N], [N2]) :- 
 detect_number(N, N2).
detect_all([N,O|T], [N2,O2|T2]) :- 
 detect_number(N, N2), 
 detect_operator(O, O2), 
 detect_all(T, T2).
almost_equal(X, Y) :- 
 ground(Y), 
 abs(X - Y) < 0.0001.
almost_equal(X, Y) :- 
 var(Y), 
 Y is float(X).
expression(Images, Result) :- 
 detect_all(Images, Symbols), 
 parse(Symbols, Result).
parse([N], R) :- 
 almost_equal(N, R).
parse([N1, +, N2 | T], R) :-
 almost_equal(Sum, N1 + N2),
 parse([Sum | T], R).
parse([N1, -, N2 | T], R) :-
 almost_equal(Diff, N1 - N2),
 parse([Diff | T], R).
parse([N1, *, N2 | T], R) :-
 almost_equal(Prod, N1 * N2),
 parse([Prod | T], R).
parse([N1, /, N2 | T], R) :-
 N2 =\= 0,
 almost_equal(Quot, N1 / N2),
 parse([Quot | T], R).
query(expression([image_2, image_divide, image_3, image_plus, image_3, image_minus, image_2, image_multiply, image_7], X)).
/* %%% Result %%% 
Error evaluating Problog model:
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_builtin.py", line 817, in _builtin_lt
    check_mode((arg1, arg2), ["gg"], functor="<", **kwdargs)
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_builtin.py", line 630, in check_mode
    raise CallModeError(functor, args, accepted, location=location)
problog.engine_builtin.CallModeError: Invalid argument types for call to '</2': arguments: (abs(X1-2/3), 0.0001), expected: (ground, ground) at 23:13.
*/