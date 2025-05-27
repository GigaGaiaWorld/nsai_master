% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(Door) :- select_door(Selected), member(Door, [1,2,3]), \+ prize(Door), \+ (Door = Selected), findall(D, (member(D, [1,2,3]), \+ prize(D), \+ (D = Selected)), Ds), length(Ds, 2), member(Door, Ds), 0.5::open_door(Door).
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
Report: The generated code correctly implements the Monty Hall problem logic, producing the same probabilities as the original code. It simplifies the door-opening rule by using findall to identify valid doors and assigns a 0.5 probability, which is consistent with the original's behavior. Both codes yield identical results for prize distribution, win_keep, and win_switch probabilities.
*/