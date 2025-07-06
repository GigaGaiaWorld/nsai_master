% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(Door) :- select_door(Selected), findall(D, (member(D,[1,2,3]), \+ prize(D), D \= Selected), AvailableDoors), length(AvailableDoors, Len), (Len = 2 -> member(Door, AvailableDoors), 0.5::door_open(Door) ; Len = 1 -> member(Door, AvailableDoors), door_open(Door)).
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
Validity_form: False
Validity_result: False
Report: The generated code attempts to simplify the original Monty Hall problem implementation but introduces syntax errors and logical inconsistencies. The main issue is in the 'open_door' predicate, where it incorrectly uses '0.5::door_open(Door)' instead of '0.5::open_door(Door)', leading to an 'UnknownClause' error. The original code correctly models the problem with proper probability distributions and conditions for opening doors, while the generated code fails to execute due to these errors.
*/