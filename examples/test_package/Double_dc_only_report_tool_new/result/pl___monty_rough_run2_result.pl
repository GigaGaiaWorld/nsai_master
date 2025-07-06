% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(Door) :- select_door(Selected), findall(D, (member(D, [1,2,3]), \+ prize(D), D \= Selected), AvailableDoors), length(AvailableDoors, Len), (Len = 2 -> (random(0.5) -> nth0(0, AvailableDoors, Door) ; nth0(1, AvailableDoors, Door) ; Len = 1 -> nth0(0, AvailableDoors, Door)).
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
Report: The generated code is not valid due to a syntax error in the 'open_door' predicate, specifically an unmatched parenthesis. This prevents the code from running successfully. The original code correctly implements the Monty Hall problem logic, with proper probabilistic rules for opening doors and calculating win probabilities for both keeping and switching choices. The generated code fails to replicate this functionality due to its syntactic errors.
*/