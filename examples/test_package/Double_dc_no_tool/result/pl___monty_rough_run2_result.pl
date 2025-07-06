% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(D) :- select_door(Selected), findall(X, (member(X,[1,2,3]), X \= Selected, \+ prize(X)), Doors), (   Doors = [A,B] -> 0.5::open_door(A) ; 0.5::open_door(B) ;   Doors = [A] -> open_door(A) ).
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
Report: The generated code attempts to simplify the original code but introduces syntax errors, particularly in the 'open_door' predicate where the conditional operator '->' is incorrectly used. This makes the generated code invalid and unable to run, unlike the original code which executes correctly and produces the expected Monty Hall problem probabilities. The generated code fails to maintain the logical structure and probabilistic rules of the original, leading to a runtime error.
*/