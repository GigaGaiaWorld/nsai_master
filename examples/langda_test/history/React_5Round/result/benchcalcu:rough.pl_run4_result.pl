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
 
leftdigit(A), leftdigit(C),
    digit(B), digit(D), digit(E),
    all_different([A,B,C,D,E]),
    % AB + BCD = CDE
    % Break down into column-wise addition
    % Units place: B + D = E (with possible carry)
    sumdigit(0, B, D, E, C1),
    % Tens place: A + C = D (with carry from units and possible new carry)
    sumdigit(C1, A, C, D, C2),
    % Hundreds place: 0 + B = C (with carry from tens)
    sumdigit(C2, 0, B, C, _).
% Initiate query example:
query(query_sum([A,B,C,D,E])).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is mostly correct and consistent with the original code in terms of functionality. Both codes solve the cryptoaddition problem AB + BCD = CDE with the same constraints. However, the generated code has a minor formatting issue with the digit predicates being split across lines unnecessarily. The logic and constraints remain intact, and the running results are identical, indicating that the generated code meets the requirements.
*/