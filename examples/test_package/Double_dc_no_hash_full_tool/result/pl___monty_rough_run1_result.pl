% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(Door) :-    select_door(Selected),    prize(Prize),    findall(D, (member(D, [1,2,3]), \+ D = Selected, \+ D = Prize), Doors),    length(Doors, N),    (N =:= 2 ->        random_member(Door, Doors)    ; N =:= 1 ->        member(Door, Doors)    ).
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
Report: The generated code attempts to simplify the original Monty Hall problem implementation but introduces errors. The main issue is in the 'open_door' predicate, which uses undefined predicates 'random_member' and incorrect logic for door selection. This makes the generated code invalid as it cannot be executed. The original code correctly models the problem with proper probability distributions and door opening logic, yielding the expected results (1/3 chance for win_keep and 2/3 for win_switch).
*/