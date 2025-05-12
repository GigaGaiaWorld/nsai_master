zebra(Houses) :-
 houses(Houses),
 

% 1. The Englishman lives in the red house.
my_member(house(englishman, _, _, red, _), Houses),

% 2. The Spaniard owns the dog.
my_member(house(spaniard, dog, _, _, _), Houses),

% 3. The owner of the green house drinks coffee.
my_member(house(_, _, coffee, green, _), Houses),

% 4. The Ukrainian drinks tea.
my_member(house(ukrainian, _, tea, _, _), Houses),

% 5. The green house is to the right of the ivory house.
right_of(house(_, _, _, green, _), house(_, _, _, ivory, _), Houses),

% 6. The Winston smoker keeps snails.
my_member(house(_, snails, _, _, winston), Houses),

% 7. The Kools are smoked in the yellow house.
my_member(house(_, _, _, yellow, kools), Houses),

% 8. Milk is in the middle (third) house.
Houses = [_, _, house(_, milk, _, _, _), _, _],

% 9. The Norwegian lives in the first house.
Houses = [house(norwegian, _, _, _, _)|_],

% 10. The man who smokes Chesterfields lives next to the one who keeps a fox.
next_to(house(_, _, _, _, chesterfield), house(_, fox, _, _, _), Houses),

% 11. The man who smokes Kools lives next to the one who keeps a horse.
next_to(house(_, _, _, _, kools), house(_, horse, _, _, _), Houses),

% 12. The Lucky Strikes smoker drinks orange juice.
my_member(house(_, orange_juice, _, _, lucky_strikes), Houses),

% 13. The Japanese smokes Parliaments.
my_member(house(japanese, _, _, _, parliaments), Houses),

% 14. The Norwegian lives next to the blue house.
next_to(house(norwegian, _, _, _, _), house(_, _, _, blue, _), Houses),

% 15. One of the householders keeps a zebra.
my_member(house(_, zebra, _, _, _), Houses),

% 16. One of the householders drinks water.
my_member(house(_, water, _, _, _), Houses).

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
zebra(X2) = 0.0000