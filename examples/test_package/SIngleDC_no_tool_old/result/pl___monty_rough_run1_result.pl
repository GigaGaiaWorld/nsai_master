% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(D) :-    select_door(Selected),    findall(X, (member(X,[1,2,3]), \+ prize(X), X \= Selected), [A,B]),    D = A.
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
Report: The generated code simplifies the original code by changing the way doors are opened. Instead of probabilistic selection between two non-prize, non-selected doors, it deterministically picks the first available non-prize, non-selected door. Despite this change in implementation, the core logic remains consistent with the Monty Hall problem, and the results match the original probabilities for both keeping and switching choices.
*/