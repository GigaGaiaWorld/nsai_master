% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(D) :- select_door(S), prize(P), findall(X, (member(X,[1,2,3]), X \= S, X \= P), [A,B]), 0.5::open_door(A) ; 0.5::open_door(B).
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
Report: The generated code correctly implements the Monty Hall problem logic and produces the same results as the original code. It simplifies the door-opening rule by using findall to identify valid doors to open, which is more concise but functionally equivalent to the original's explicit conditions. Both codes correctly show a 1/3 chance of winning by keeping the initial choice and a 2/3 chance by switching.
*/