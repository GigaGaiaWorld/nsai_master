% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(Door) :- select_door(Selected), find_available_doors(Selected, Available), random_select(Available, Door). find_available_doors(Selected, Available) :- findall(D, (member(D, [1,2,3]), \+ prize(D), D \= Selected), Available), length(Available, Len), (Len =:= 2 -> true ; length(Available, 1)). random_select([A,B], D) :- 0.5::door_choice(A) ; 0.5::door_choice(B), door_choice(D). random_select([A], A).
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
Report: The generated code attempts to replicate the Monty Hall problem logic but contains syntax errors, specifically an operator priority clash, making it invalid. The original code correctly models the problem with proper probabilistic rules and queries, yielding expected results (win_keep: 0.3333, win_switch: 0.6667). The generated code fails to execute due to parsing errors, indicating it does not meet the requirements.
*/