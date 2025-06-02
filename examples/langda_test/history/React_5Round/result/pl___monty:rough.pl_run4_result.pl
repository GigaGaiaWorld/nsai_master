% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(D) :-
    select_door(Selected),
    findall(X, (member(X,[1,2,3]), X \= Selected, \+ prize(X)), PossibleDoors),
    (length(PossibleDoors, 2) -> 
        0.5::open_door(D), member(D, PossibleDoors) ;
    member(D, PossibleDoors)).
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
Report: The generated code attempts to replicate the Monty Hall problem logic but contains a syntax error in the 'open_door' rule, specifically an operator priority clash. This makes the code invalid and unable to run. The original code correctly implements the problem with proper probability distributions and rules, producing expected results (win_keep=0.3333, win_switch=0.6667). The generated code fails to meet the requirements due to its syntax error.
*/