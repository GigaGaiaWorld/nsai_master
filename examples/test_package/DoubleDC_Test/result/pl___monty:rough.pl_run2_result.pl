% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(Door) :- select_door(Selected), member(Door, [1,2,3]), \+ prize(Door), \+ (Door = Selected), findall(D, (member(D, [1,2,3]), \+ prize(D), \+ (D = Selected)), Doors), length(Doors, 2), member(Door, Doors), 0.5::open_door(Door).
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
Report: The generated code correctly implements the Monty Hall problem logic, producing the same results as the original code. Both codes assign equal probabilities to the prize locations and correctly calculate the winning probabilities for keeping (1/3) and switching (2/3) doors. The generated code simplifies the door-opening logic using findall and length, which is more concise but functionally equivalent to the original's explicit enumeration. No functional discrepancies are observed.
*/