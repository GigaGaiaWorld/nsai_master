% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 
select_door(D), member(A,[1,2,3]), \+ select_door(A), member(B,[1,2,3]), \+ select_door(B), A \= B, \+ prize(A), \+ prize(B)
.
open_door(A) :-
 
select_door(D), member(A,[1,2,3]), \+ select_door(A), member(B,[1,2,3]), \+ select_door(B), A \= B, prize(A), \+ prize(B)
.
win_keep :-
 
select_door(D), prize(D)
.
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
Validity_result: False
Report: The generated code has significant issues compared to the original code. The main problem lies in the 'open_door' and 'win_switch' predicates. The generated code incorrectly modifies the conditions for opening a door and checking for a win when switching, leading to a 'win_switch' probability of 0.0000, which contradicts the expected Monty Hall problem solution where 'win_switch' should be 0.6667. The original code correctly implements the problem's logic, while the generated code fails to maintain this logic.
*/