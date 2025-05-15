% Cryptoaddition:
% Find the unique answer to:
query_sum([S,E,N,D,M,O,R,Y]) :-
 
digit(D), digit(E), D =\= E
,
 
sumdigit(0, D, E, Y, C1)
,
 
digit(N), all_different([N,Y,E,D])
,
 
digit(R), all_different([R,N,Y,E,D])
,
 
sumdigit(C1, N, R, E, C2)
,
 
digit(O), all_different([O,R,N,Y,E,D])
,
 
sumdigit(C2, E, O, N, C3)
,
 
leftdigit(S), all_different([S,O,R,N,Y,E,D])
,
 
leftdigit(M), all_different([M,S,O,R,N,Y,E,D])
,
 
sumdigit(C3, S, M, O, M)
,
 sumdigit(0, D, E, Y, C1),
 % 为 R 赋值，并确保它与之前所有字母不同
 digit(R), all_different([R,N,Y,E,D]),
 % 计算十位数 N + R + C1 = E（带入进位 C2）
 sumdigit(C1, N, R, E, C2),
 % 为 O 赋值，确保不与已有字母重复
 digit(O), all_different([O,R,N,Y,E,D]),
 % 计算百位数 E + O + C2 = N（带入进位 C3）
 sumdigit(C2, E, O, N, C3),
 % S 是 SEND 的最高位，不能为 0，确保唯一
 leftdigit(S), all_different([S,O,R,N,Y,E,D]),
 % M 是 MORE 和 MONEY 的最高位，不能为 0，确保唯一
 leftdigit(M), all_different([M,S,O,R,N,Y,E,D]),
 % 计算千位数 S + M + C3 = O，并将进位结果限制为 M（即最高位为 M）
 sumdigit(C3, S, M, O, M),
 sumdigit(C3, S, M, O, M),
 
 all_different([S,E,N,D,M,O,R,Y]).
sumdigit(C, A, B, S, 0) :-
 X is C + A + B,
 X < 10,
 S = X.
sumdigit(C, A, B, S, 1) :-
 X is C + A + B,
 X >= 10,
 S is X - 10.
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
leftdigit(D) :- digit(D), D =\= 0.
all_different([]).
all_different([H|T]) :- \+ member(H, T), all_different(T).
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).
query(query_sum(X)).

*** Result:*** 
% Problog Inference Result：
query_sum([9, 5, 6, 7, 1, 0, 8, 2]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is functionally equivalent to the original code and produces the same result. However, it contains redundant lines and comments that do not affect the execution but make the code less clean. The core logic, constraints, and digit assignments remain consistent between both versions. The generated code correctly solves the cryptarithmetic puzzle with the same output as the original.