% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 
member(A,[1,2,3]), member(B,[1,2,3]), A < B, \+ select_door(A), \+ select_door(B), \+ prize(A), \+ prize(B)
.
open_door(A) :-
 
member(A,[1,2,3]), member(B,[1,2,3]), A < B, \+ select_door(A), \+ select_door(B), \+ prize(A), prize(B)
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
Validity_result: True
Report: The generated code is mostly correct and consistent with the original code in terms of functionality and logic. It correctly implements the Monty Hall problem, with the same probability distributions and rules. However, there is a minor inconsistency in the 'open_door' predicate where the condition 'A < B' is included in the second clause, which was not present in the original code. This does not affect the results in this specific case but could potentially lead to different behaviors in other scenarios. The running results of both codes are identical, confirming that the generated code meets the expected outcomes.
*/