% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 
select_door(S), member(A,[1,2,3]), member(B,[1,2,3]), A < B, \+ prize(A), \+ prize(B), \+ select_door(A), \+ select_door(B)
.
open_door(A) :-
 
select_door(S), member(A,[1,2,3]), \+ select_door(A), \+ prize(A), \+ (member(B,[1,2,3]), \+ select_door(B), \+ prize(B), B \= A)
.
win_keep :-
 select_door(A),
 prize(A).
win_switch :-
 member(A, [1,2,3]),
 \+ select_door(A),
 prize(A),
 \+ open_door(A).
query(prize(_)).
query(select_door(_)).
query(win_keep).
query(win_switch).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is mostly correct and maintains the same functionality as the original code. It correctly implements the Monty Hall problem logic, with the same probability distributions for the prize, door selection, and outcomes (win_keep and win_switch). However, the generated code introduces an unnecessary variable 'S' in the open_door rules, which is not used in the body of the rules. This does not affect the results but is a minor inconsistency in form. The running results of both codes are identical, confirming that the generated code produces the correct probabilities.
*/