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
parse([N1, *, N2 | T], R) :- 
    Temp is N1 * N2,
    parse([Temp | T], R).
parse([N1, /, N2 | T], R) :- 
    Temp is N1 / N2,
    parse([Temp | T], R).
parse([N1, +, N2 | T], R) :- 
    Temp is N1 + N2,
    parse([Temp | T], R).
parse([N1, -, N2 | T], R) :- 
    Temp is N1 - N2,
    parse([Temp | T], R).
% calculate with almost equal: 2 / (3 + 3) - 2 * 7
query(expression([image_2, image_divide, image_3, image_plus, image_3, image_minus, image_2, image_multiply, image_7], X)).

/* Result Report:
Validity_form: True
Validity_result: False
Report: The generated code is not consistent with the original code in terms of parsing logic. The original code handles subtraction by converting it into addition with a negative value, while the generated code directly performs subtraction. This leads to different results for the same input. The generated code's result (11.666...) is incorrect for the given expression (2 / (3 + 3) - 2 * 7), which should evaluate to approximately -10.333. The generated code is syntactically valid but semantically incorrect for the intended operation.
*/