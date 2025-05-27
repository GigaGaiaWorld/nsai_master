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
parse([N1, Op, N2 | Rest], R) :- 
    (Op = * ; Op = /), 
    almost_equal(N1, X1), 
    almost_equal(N2, X2), 
    (Op = * -> Temp is X1 * X2 ; Temp is X1 / X2), 
    parse([Temp | Rest], R).

parse([N1, Op, N2 | Rest], R) :- 
    (Op = + ; Op = -), 
    almost_equal(N1, X1), 
    almost_equal(N2, X2), 
    (Op = + -> Temp is X1 + X2 ; Temp is X1 - X2), 
    parse([Temp | Rest], R).
query(expression([image_2, image_divide, image_3, image_plus, image_3, image_minus, image_2, image_multiply, image_7], X)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code attempts to simplify the parsing logic by combining the operations into two clauses for multiplication/division and addition/subtraction. However, it fails to handle the case where the operator is part of a larger expression chain, leading to an 'UnknownClause' error. The original code correctly processes the expression by recursively parsing each part, while the generated code lacks the necessary recursive structure to handle complex expressions.
*/