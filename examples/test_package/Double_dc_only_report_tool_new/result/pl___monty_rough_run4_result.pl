% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
find_available_doors(Selected, Available) :-    findall(D, (member(D,[1,2,3]), \+ prize(D), \+ D=Selected), Available).

open_door(Door) :-    select_door(Selected),    find_available_doors(Selected, Available),    (length(Available, 2) ->         random_member(Door, Available)     ;         Available=[Door]    ).
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
Report: The generated code attempts to simplify the original Monty Hall problem implementation but introduces errors. The main issue is with the 'open_door' predicate, which incorrectly uses 'random_member' without proper definition, leading to a runtime error. The original code correctly handles door opening with probabilistic choices, while the generated version fails to execute due to undefined predicates. The logic for 'win_keep' and 'win_switch' remains consistent, but the overall implementation is invalid due to the execution error.
*/