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
parse([N1,+|T], R) :-
    parse(T, R2),
    almost_equal(R, N1 + R2).
parse([N1,-|T], R) :-
    parse(T, R2),
    almost_equal(R, N1 - R2).
parse([N1,*|T], R) :-
    parse(T, R2),
    almost_equal(R, N1 * R2).
parse([N1,/|T], R) :-
    parse(T, R2),
    almost_equal(R, N1 / R2).
% calculate with almost equal: 2 / (3 + 3) - 2 * 7
query(expression([image_2, image_divide, image_3, image_plus, image_3, image_minus, image_2, image_multiply, image_7], X)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code modifies the parsing logic for arithmetic operations, particularly changing how subtraction and division are handled. Unlike the original code, it doesn't properly handle operator precedence and grouping (like parentheses in the expression '2 / (3 + 3) - 2 * 7'). This leads to incorrect evaluation order and ultimately causes a runtime error due to unground variables in the 'almost_equal' predicate. The original code correctly handles the expression by maintaining proper operator precedence.
*/