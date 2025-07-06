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
    digit(D),
    digit(E)
,
 
sumdigit(0, D, B, E, Carry1)
,
 
sumdigit(Carry1, C, B, D, Carry2)
,
 
sumdigit(Carry2, B, A, C, Carry3),
    Carry3 = 0
,
 
all_different([A,B,C,D,E])
.
% Initiate query example:
query(query_sum([A,B,C,D,E])).
/* %%% Result %%% 
% Problog Inference Result：
query_sum([1, 2, 3, 5, 7]) = 1.0000
query_sum([2, 1, 3, 4, 5]) = 1.0000
query_sum([2, 4, 7, 1, 5]) = 1.0000
query_sum([3, 1, 4, 5, 6]) = 1.0000
query_sum([3, 2, 5, 7, 9]) = 1.0000
query_sum([3, 2, 5, 8, 0]) = 1.0000
query_sum([3, 4, 8, 2, 6]) = 1.0000
query_sum([4, 1, 5, 6, 7]) = 1.0000
query_sum([4, 2, 6, 9, 1]) = 1.0000
query_sum([5, 1, 6, 7, 8]) = 1.0000
query_sum([6, 1, 7, 8, 9]) = 1.0000
query_sum([6, 1, 7, 9, 0]) = 1.0000
query_sum([6, 2, 9, 1, 3]) = 1.0000
*/