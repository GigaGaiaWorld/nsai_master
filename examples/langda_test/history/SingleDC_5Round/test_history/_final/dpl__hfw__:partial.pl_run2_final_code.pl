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
 
detect_all(Images, Parsed),
    parse(Parsed, Result).
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

*** Result:*** 
% Problog Inference Result：
expression([image_2, image_divide, image_3, image_plus, image_3, image_minus, image_2, image_multiply, image_7],-10.333333333333332) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is largely consistent with the original code in terms of functionality and structure. It correctly implements the number and operator detection, parsing, and evaluation logic. The only minor issue is the formatting inconsistency in the 'detect_all' predicate where the line breaks and indentation are not perfectly aligned, but this does not affect the code's functionality. The running results of both codes are identical, producing the same output for the given query.