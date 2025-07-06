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

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code modifies the parsing logic by attempting to evaluate binary operations immediately rather than handling operator precedence correctly. This leads to incorrect parsing of expressions with multiple operators. The error in the run result indicates a problem with the 'almost_equal' predicate, which fails because it's being called with non-ground arguments. The original code correctly handles operator precedence by recursively parsing sub-expressions, while the generated code does not.
*/