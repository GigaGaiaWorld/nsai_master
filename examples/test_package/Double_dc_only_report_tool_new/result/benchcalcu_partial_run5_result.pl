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
 
leftdigit(A), % First digit of AB cannot be 0
    leftdigit(B), % First digit of BCD cannot be 0
    leftdigit(C), % First digit of CDE cannot be 0
    digit(D),
    digit(E)
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
Report: The generated code is functionally equivalent to the original code, with only minor formatting differences and a slight reorganization of the constraints in the query_sum predicate. The logic for digit definitions, leftdigit, all_different, member, and sumdigit remains unchanged. The query_sum predicate in the generated code is split into multiple lines for clarity but maintains the same constraints and operations as the original. The running results of both codes are identical, confirming that the generated code meets the requirements.
*/