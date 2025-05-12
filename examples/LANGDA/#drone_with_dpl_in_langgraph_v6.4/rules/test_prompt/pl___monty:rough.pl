% Based on Monty Hall problem on https://github.com/friguzzi/cplint

1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).

select_door(1).

member(X,[X|T]).
member(X,[H|T]) :- member(X,T).

langda(LLM:"Define open_door/1 Predicate:

Random Door Opening Rules

Scenario: The remaining two doors are neither selected by the player nor have any prizes.

Behavior: The host randomly opens one of the two "empty doors" with a 50% probability.

Deterministic Door Opening Rules

Scenario: The remaining two doors are neither selected by the player, one of which has a prize and the other does not.

Behavior: The host must open the "empty door".").

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