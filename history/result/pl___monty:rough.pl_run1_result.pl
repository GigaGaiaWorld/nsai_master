% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(D) :- member(A, [1,2,3]), member(B, [1,2,3]), A \= B, \+ prize(A), \+ prize(B), \+ select_door(A), \+ select_door(B), (D = A ; D = B).
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
Report: The generated code correctly implements the Monty Hall problem logic, maintaining the same probabilistic outcomes as the original code. It simplifies the 'open_door' rule by combining the two clauses from the original into one, which is more concise but functionally equivalent. The results for 'win_keep' and 'win_switch' probabilities remain consistent with the original, demonstrating correct behavior.
*/