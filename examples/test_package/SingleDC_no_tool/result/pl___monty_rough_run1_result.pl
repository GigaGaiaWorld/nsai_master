% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(Door) :- select_door(Selected), findall(D, (member(D,[1,2,3]), \+ prize(D), D \= Selected), AvailableDoors), length(AvailableDoors, Len), (Len = 2 -> member(Door, AvailableDoors), 0.5::open_door(Door) ; Len = 1 -> [AvailableDoor] = AvailableDoors, Door = AvailableDoor ).
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
Report: The generated code attempts to simplify the original Monty Hall problem implementation but introduces syntax errors, particularly in the 'open_door' predicate where the probabilistic choice is incorrectly formatted. This leads to a runtime error ('UnknownClause'), indicating the code is not valid. The original code correctly models the problem with proper probabilistic choices and yields expected results (win_keep: 0.3333, win_switch: 0.6667). The generated code fails to execute, thus not meeting the requirements.
*/