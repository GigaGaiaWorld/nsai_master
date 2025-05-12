

zebra(Houses) :-
    houses(Houses),
    langda(LLM:"
1. The Englishman lives in the red house.
2. The Spaniard owns the dog.
3. The owner of the green house drinks coffee.
4. The Ukrainian drinks tea.
5. The green house is to the right of the ivory house.
6. The Winston smoker keeps snails.
7. The Kools are smoked in the yellow house.
8. Milk is in the middle (third) house.
9. The Norwegian lives in the first house.
10. The man who smokes Chesterfields lives next to the one who keeps a fox.
11. The man who smokes Kools lives next to the one who keeps a horse.
12. The Lucky Strikes smoker drinks orange juice.
13. The Japanese smokes Parliaments.
14. The Norwegian lives next to the blue house.
15. One of the house­holders keeps a zebra.
16. One of the house­holders drinks water.
")

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