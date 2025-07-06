zebra(Houses) :-
	houses(Houses),
	
my_member(house(english, red, _, _, _), Houses),
    my_member(house(spanish, _, _, _, dog), Houses),
    my_member(house(_, green, coffee, _, _), Houses),
    my_member(house(ukrainian, _, tea, _, _), Houses),
    right_of(house(_, green, _, _, _), house(_, ivory, _, _, _), Houses),
    my_member(house(_, _, _, winstons, snail), Houses),
    my_member(house(_, yellow, _, kools, _), Houses),
    Houses = [_, _, house(_, _, milk, _, _), _, _],
    Houses = [house(norwegian, _, _, _, _) | _],
    next_to(house(_, _, _, chesterfields, _), house(_, _, _, _, fox), Houses),
    next_to(house(_, _, _, kools, _), house(_, _, _, _, horse), Houses),
    my_member(house(_, _, orange_juice, lucky_strikes, _), Houses),
    my_member(house(japanese, _, _, parliaments, _), Houses),
    next_to(house(norwegian, _, _, _, _), house(_, blue, _, _, _), Houses),
    my_member(house(_, _, water, _, _), Houses),
    my_member(house(_, _, _, _, zebra), Houses).
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
zebra([house(norwegian,yellow,water,kools,fox), house(ukrainian,blue,tea,chesterfields,horse), house(english,red,milk,winstons,snail), house(spanish,ivory,orange_juice,lucky_strikes,dog), house(japanese,green,coffee,parliaments,zebra)]) = 1.0000
*/