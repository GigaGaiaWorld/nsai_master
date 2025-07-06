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
 
leftdigit(A),
    leftdigit(B),
    leftdigit(C),
    digit(B),
    digit(C),
    digit(D),
    digit(E)
,
 
sumdigit(0, B, D, E, Carry1)
,
 
sumdigit(Carry1, A, C, D, Carry2)
,
 
sumdigit(Carry2, 0, B, C, Carry3),
    Carry3 = 0
,
 
all_different([A,B,C,D,E])
.
% Initiate query example:
query(query_sum([A,B,C,D,E])).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is functionally equivalent to the original code, producing the same results for the cryptoaddition problem. Both codes correctly implement the constraints and logic for solving AB + BCD = CDE with unique digits. The generated code has minor formatting differences (spacing and line breaks) and adds redundant digit checks for B and C (which are already covered by leftdigit), but these do not affect the logic or results. The generated code also explicitly names the carry variables (Carry1, Carry2, Carry3) and adds a check for Carry3 = 0, which is consistent with the original's implicit requirement of no final carry.
*/