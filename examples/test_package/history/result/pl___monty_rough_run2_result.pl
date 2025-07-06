% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_available(1, [A], A).
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
Report: The generated code is incomplete and incorrect. It misses the crucial 'open_door' predicate definitions which are essential for the Monty Hall problem simulation. The original code properly defines when doors can be opened based on prize locations and player selection, while the generated code only includes a stub 'open_available' that doesn't serve the same purpose. This causes a runtime error when trying to evaluate 'open_door/1'. The generated code fails to maintain the core logic of the original problem.
*/