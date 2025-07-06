% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(Door) :- select_door(Selected), findall(X, (member(X, [1,2,3]), \+ prize(X), \+ X = Selected), Doors), length(Doors, 2), member(Door, Doors).
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
Report: The generated code correctly implements the Monty Hall problem logic, producing the same results as the original code. It simplifies the door-opening mechanism by using findall to identify non-prize, non-selected doors, which is more concise but equally effective. Both codes maintain the same probability distributions for prize selection, door selection, and winning outcomes (keep vs switch).
*/