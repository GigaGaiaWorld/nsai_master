% Cryptoaddition:
% Find the unique answer to:

% Define available digits
digit(0). digit(1). digit(2). digit(3). digit(4).
digit(5). digit(6). digit(7). digit(8). digit(9).

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
    % Define the digits and first digits should be non-zero
    leftdigit(A),
    leftdigit(B),
    leftdigit(C),
    digit(D),
    digit(E),
    
    % Compute units digit (B + D = E with possible carry)
    sumdigit(0, B, D, E, Carry1),
    
    % Compute tens digit (A + C + Carry1 = D with possible carry)
    sumdigit(Carry1, A, C, D, Carry2),
    
    % Compute hundreds digit (0 + B + Carry2 = C)
    sumdigit(Carry2, 0, B, C, _),
    
    % Make sure all letters are different
    all_different([A,B,C,D,E]).

% Initiate query example:
query(query_sum([A,B,C,D,E])).




*** Result:*** 
% Problog Inference Result：
query_sum([4, 7, 8, 2, 9]) = 1.0000
query_sum([4, 7, 8, 3, 0]) = 1.0000
query_sum([5, 6, 7, 2, 8]) = 1.0000
query_sum([5, 7, 8, 4, 1]) = 1.0000
query_sum([6, 7, 8, 5, 2]) = 1.0000
query_sum([7, 4, 5, 2, 6]) = 1.0000
query_sum([7, 5, 6, 3, 8]) = 1.0000
query_sum([8, 3, 4, 2, 5]) = 1.0000
query_sum([8, 4, 5, 3, 7]) = 1.0000
query_sum([8, 5, 6, 4, 9]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality and logic. Both codes implement the same cryptarithmetic puzzle (AB + BCD = CDE) with identical constraints and digit addition rules. The generated code maintains the same structure for digit definitions, leftdigit checks, sumdigit calculations, and all_different constraints. The only minor differences are in formatting and variable naming (Carry1 vs C1, Carry2 vs C2), which do not affect the logic. The running results of both codes are identical, producing the same set of valid solutions with the same probabilities.