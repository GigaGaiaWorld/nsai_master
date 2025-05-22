zebra(Houses) :-
 houses(Houses),
 
member(house(englishman, _, _, red, _), Houses),
member(house(spaniard, dog, _, _, _), Houses),
member(house(_, _, coffee, green, _), Houses),
member(house(ukrainian, _, tea, _, _), Houses),
right_of(house(_, _, _, green, _), house(_, _, _, ivory, _), Houses),
member(house(_, snails, _, _, winston), Houses),
member(house(_, _, _, yellow, kools), Houses),
Houses = [_, _, house(_, _, milk, _, _), _, _],
Houses = [house(norwegian, _, _, _, _)|_],
next_to(house(_, _, _, _, chesterfields), house(_, fox, _, _, _), Houses),
next_to(house(_, _, _, _, kools), house(_, horse, _, _, _), Houses),
member(house(_, _, orange_juice, _, lucky_strikes), Houses),
member(house(japanese, _, _, _, parliaments), Houses),
next_to(house(norwegian, _, _, _, _), house(_, _, _, blue, _), Houses),
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