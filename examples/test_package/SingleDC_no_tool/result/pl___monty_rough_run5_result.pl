% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(Door) :-    select_door(Selected),    findall(D, (member(D,[1,2,3]), \+ prize(D), D \= Selected), Available),    length(Available, Len),    (Len = 2 ->         random_member(Door, Available)    ;        Len = 1 ->         [Door] = Available    ).
random_member(X, [X,_]) :- 0.5.
random_member(X, [_,X]) :- 0.5.
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
Report: The generated code attempts to replicate the Monty Hall problem logic but introduces errors. The main issue is with the 'random_member' predicate, which is incorrectly defined and causes a runtime error ('UnknownClause'). The original code uses probabilistic rules for door opening, while the generated code tries to implement a deterministic approach with random selection, but fails due to syntax/logic errors. The generated code does not produce valid results and is not consistent with the original code's behavior.
*/