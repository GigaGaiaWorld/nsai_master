% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(Door) :- select_door(Selected), findall(D, (member(D,[1,2,3]), \+ prize(D), D \= Selected), Available), length(Available, Len), (Len =:= 2 -> random_select(Door, Available) ; Len =:= 1 -> [Door|_] = Available).
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
Report: The generated code attempts to simplify the original Monty Hall problem implementation but introduces errors. The main issue is in the 'open_door' predicate, which uses undefined predicates 'random_select' and incorrect logic for door selection. This makes the generated code invalid and unable to run. The original code correctly models the problem with proper probability distributions and door-opening rules, producing the expected results (win_keep=0.3333, win_switch=0.6667). The generated code fails to replicate this behavior due to its syntactic and logical errors.
*/