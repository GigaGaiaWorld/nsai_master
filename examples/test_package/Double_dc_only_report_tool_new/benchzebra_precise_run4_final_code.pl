zebra(Houses) :-
	houses(Houses),
	
my_member(house(english, red, _, _, _), Houses),
    my_member(house(spanish, _, dog, _, _), Houses),
    my_member(house(_, green, _, coffee, _), Houses),
    my_member(house(ukrainian, _, _, tea, _), Houses),
    right_of(house(_, green, _, _, _), house(_, ivory, _, _, _), Houses),
    my_member(house(_, _, snail, _, winstons), Houses),
    my_member(house(_, yellow, _, _, kools), Houses),
    Houses = [_, _, house(_, _, _, milk, _), _, _],
    Houses = [house(norwegian, _, _, _, _) | _],
    next_to(house(_, _, _, _, chesterfields), house(_, _, fox, _, _), Houses),
    next_to(house(_, _, _, _, kools), house(_, _, horse, _, _), Houses),
    my_member(house(_, _, _, orange_juice, lucky_strikes), Houses),
    my_member(house(japanese, _, _, _, parliaments), Houses),
    next_to(house(norwegian, _, _, _, _), house(_, blue, _, _, _), Houses),
    my_member(house(_, _, zebra, _, _), Houses),
    my_member(house(_, _, _, water, _), Houses)
.
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
/* %%% Result %%% 
% Problog Inference Result：
zebra([house(norwegian,yellow,fox,water,kools), house(ukrainian,blue,horse,tea,chesterfields), house(english,red,snail,milk,winstons), house(spanish,ivory,dog,orange_juice,lucky_strikes), house(japanese,green,zebra,coffee,parliaments)]) = 1.0000
*/