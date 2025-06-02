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
 
leftdigit(A), digit(B), leftdigit(C), digit(D), digit(E)
,
 
sumdigit(0, B, D, E, Cout1)
,
 
sumdigit(Cout1, A, C, D, Cout2)
,
 
sumdigit(Cout2, 0, B, C, _)
,
 
all_different([A,B,C,D,E])
.
% Initiate query example:
query(query_sum([A,B,C,D,E])).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is largely consistent with the original code in terms of functionality and logic. Both codes aim to solve the same cryptoaddition problem (AB + BCD = CDE) with the same constraints. The generated code correctly maintains the digit definitions, leftdigit constraints, sumdigit logic, and all_different checks. The main difference is in the formatting and minor syntactic variations (like spacing and line breaks), which do not affect the logic or execution. The running results of both codes are identical, producing the same set of valid solutions.
*/