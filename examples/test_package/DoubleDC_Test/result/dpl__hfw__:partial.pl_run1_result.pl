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
 
detect_all(Images, List),
    parse(List, Result).
parse([N], R) :- 
 almost_equal(N, R).
parse([N1,+|T], R) :-
 parse(T, R2),
 almost_equal(N1 + R2, R).
parse([N1,-|T], R) :-
 parse([-1, *|T], R2),
 almost_equal(N1 + R2, R).
parse([N1,*,N2|T], R) :-
 N3 is N1 * N2,
 parse([N3|T], R).
parse([N1,/,N2|T], R) :-
 N2 \== 0,
 N3 is N1 / N2,
 parse([N3|T], R).
% calculate: 2 / (3 + 3) - 2 * 7
query(expression([image_2, image_divide, image_3, image_plus, image_3, image_minus, image_2, image_multiply, image_7], X)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is largely consistent with the original code in terms of functionality and structure. Both codes correctly implement the detection of numbers and operators, and the parsing of expressions to compute the result. The generated code maintains the same logic for parsing and evaluating expressions, including handling of arithmetic operations and the almost_equal predicate. The only minor difference is in the formatting and spacing, which does not affect the functionality. The running results of both codes are identical, confirming that the generated code meets the expectations.
*/