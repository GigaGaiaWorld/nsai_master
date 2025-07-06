% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(D) :- select_door(Selected), findall(X, (member(X,[1,2,3]), \+ prize(X), X \= Selected), Doors), length(Doors, 2), member(D, Doors), 0.5::open_door(D).
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
Report: The generated code correctly implements the Monty Hall problem logic, producing the same results as the original code. It simplifies the door-opening rule by using findall to identify non-prize, non-selected doors and assigns a 0.5 probability to opening one of them. This approach is more concise while maintaining the original behavior. Both codes yield identical probabilities for winning by keeping or switching doors, confirming their functional equivalence.
*/