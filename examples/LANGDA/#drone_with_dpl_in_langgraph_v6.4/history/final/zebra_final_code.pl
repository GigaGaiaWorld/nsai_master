zebra(Houses) :-
 houses(Houses),
 
my_member(house(english, _, red, _, _), Houses),
    my_member(house(spanish, dog, _, _, _), Houses),
    my_member(house(_, _, green, coffee, _), Houses),
    my_member(house(ukrainian, _, _, tea, _), Houses),
    right_of(house(_, _, green, _, _), house(_, _, ivory, _, _), Houses),
    my_member(house(_, snails, _, _, winston), Houses),
    my_member(house(_, _, yellow, _, kools), Houses),
    Houses = [_, _, house(_, _, _, milk, _), _, _],
    Houses = [house(norwegian, _, _, _, _)|_],
    next_to(house(_, _, _, _, chesterfields), house(_, fox, _, _, _), Houses),
    next_to(house(_, _, _, _, kools), house(_, horse, _, _, _), Houses),
    my_member(house(_, _, _, orange, lucky), Houses),
    my_member(house(japanese, _, _, _, parliament), Houses),
    next_to(house(norwegian, _, _, _, _), house(_, _, blue, _, _), Houses),
    my_member(house(_, zebra, _, _, _), Houses),
    my_member(house(_, _, _, water, _), Houses).
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

*** Result:*** 
% Problog Inference Result：
zebra([house(norwegian,fox,yellow,water,kools), house(ukrainian,horse,blue,tea,chesterfields), house(english,snails,red,milk,winston), house(spanish,dog,ivory,orange,lucky), house(japanese,zebra,green,coffee,parliament)]) = 1.0000