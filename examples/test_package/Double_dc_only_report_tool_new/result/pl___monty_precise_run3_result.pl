% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 
 select_door(Selected), member(A, [1,2,3]), A \= Selected, \+ prize(A), member(B, [1,2,3]), B \= Selected, B \= A, \+ prize(B), A < B.
open_door(A) :-
 
 select_door(Selected), member(A, [1,2,3]), A \= Selected, \+ prize(A), \+ (member(B, [1,2,3]), B \= Selected, B \= A, \+ prize(B)).
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
Report: The generated code is correct and consistent with the original code in terms of functionality and results. It simplifies the conditions for opening a door by explicitly stating the constraints related to the selected door and prizes, making the logic clearer. Both codes produce the same probabilities for winning by keeping or switching the choice, which are fundamental to the Monty Hall problem.
*/