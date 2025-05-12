zebra(Houses) :-
 houses(Houses),
 
member(house(englishman, _, _, _, red), Houses),
member(house(spaniard, dog, _, _, _), Houses),
member(house(_, _, coffee, _, green), Houses),
member(house(ukrainian, _, tea, _, _), Houses),
right_of(house(_, _, _, _, green), house(_, _, _, _, ivory), Houses),
member(house(_, snails, _, winston, _), Houses),
member(house(_, _, _, kools, yellow), Houses),
Houses = [_, _, house(_, _, milk, _, _), _, _],
Houses = [house(norwegian, _, _, _, _)|_],
next_to(house(_, _, _, chesterfields, _), house(_, fox, _, _, _), Houses),
next_to(house(_, _, _, kools, _), house(_, horse, _, _, _), Houses),
member(house(_, _, orange_juice, lucky_strikes, _), Houses),
member(house(japanese, _, _, parliaments, _), Houses),
next_to(house(norwegian, _, _, _, _), house(_, _, _, _, blue), Houses),
member(house(_, zebra, _, _, _), Houses),
member(house(_, _, water, _, _), Houses),
houses([
 house(_, _, _, _, _),
 house(_, _, _, _, _),
 house(_, _, _, _, _),
 house(_, _, _, _, _),
 house(_, _, _, _, _)
]).
right_of(A, B, [B, A | _]).
right_of(A, B, [_ | Y]) :- right_of(A, B, Y).
next_to(A, B, [A, B | _]).
next_to(A, B, [B, A | _]).
next_to(A, B, [_ | Y]) :- next_to(A, B, Y).
my_member(X, [X|_]).
my_member(X, [_|Y]) :- my_member(X, Y).
query(zebra(Houses)).