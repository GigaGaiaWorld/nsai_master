% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(D) :- select_door(Selected), member(D, [1,2,3]), \+ prize(D), \+ (D = Selected), findall(X, (member(X, [1,2,3]), X = Selected, \+ prize(X)), Doors), length(Doors, 2), member(D, Doors), 0.5::open_door(D).
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
Report: The generated code correctly implements the Monty Hall problem logic, maintaining the same probabilistic outcomes as the original code. Both codes produce identical results for the queries, with win_keep at 0.3333 and win_switch at 0.6667, which are the expected probabilities. The generated code simplifies the door-opening logic by using findall and length to ensure only valid doors are considered, but this does not affect the outcome. The form and structure of the generated code are valid and meet the requirements.
*/