% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 
 select_door(Selected), member(A, [1,2,3]), member(B, [1,2,3]), A \= Selected, B \= Selected, A \= B, \+ prize(A), \+ prize(B).
open_door(A) :-
 
 select_door(Selected), member(A, [1,2,3]), A \= Selected, \+ prize(A), member(B, [1,2,3]), B \= Selected, B \= A, prize(B).
win_keep :-
 
 select_door(Door), prize(Door).
win_switch :-
 member(A, [1,2,3]),
 \+ select_door(A),
 prize(A),
 \+ open_door(A).
query(prize(_)).
query(select_door(_)).
query(win_keep).
query(win_switch).

*** Result:*** 
% Problog Inference Result：
prize(1) = 0.3333
prize(2) = 0.3333
prize(3) = 0.3333
select_door(1) = 1.0000
win_keep = 0.3333
win_switch = 0.6667 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality. It accurately models the Monty Hall problem, with the same probability distributions for the prize, door selection, and outcomes (win_keep and win_switch). The generated code simplifies some conditions by explicitly stating the constraints (e.g., A \= Selected, B \= Selected) which makes it clearer while maintaining the same logical flow. The running results of both codes are identical, confirming their equivalence.