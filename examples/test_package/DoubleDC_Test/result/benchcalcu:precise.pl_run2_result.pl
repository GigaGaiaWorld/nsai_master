% Cryptoaddition:
% Find the unique answer to:
% Define available digits
digit(0).
 digit(1).
 digit(2).
 digit(3).
 digit(4).
digit(5).
 digit(6).
 digit(7).
 digit(8).
 digit(9).
% The first digit of a multi-digit number cannot be 0
leftdigit(D) :- digit(D), D =\= 0.
% All elements are different
all_different([]).
all_different([H|T]) :- \+ member(H, T), all_different(T).
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).
% Simulate a column addition: Cin is the input carry, Cout is the output carry
sumdigit(Cin, A, B, Sum, Cout) :-
 X is Cin + A + B,
 ( X < 10, Sum = X, Cout = 0
 ; 
 X >= 10, Sum is X - 10, Cout = 1 ).
% Main predicate: AB + BCD = CDE
query_sum([A,B,C,D,E]) :-
 
 leftdigit(A), leftdigit(B), leftdigit(C), digit(D), digit(E), all_different([A,B,C,D,E]), sumdigit(0, B, D, E, Carry1), sumdigit(Carry1, A, C, D, Carry2), sumdigit(Carry2, 0, B, C, Carry3), Carry3 = 0.
% Initiate query example:
query(query_sum([A,B,C,D,E])).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is functionally equivalent to the original code, producing the same results. The logic for digit constraints, sum calculations, and uniqueness checks remains consistent. However, the formatting is less readable due to inconsistent line breaks and spacing. The generated code combines some conditions on a single line, which doesn't affect functionality but reduces clarity. Both codes yield identical results, confirming correctness.
*/