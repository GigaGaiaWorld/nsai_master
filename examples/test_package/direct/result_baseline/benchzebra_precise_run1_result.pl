zebra(Houses) :-
	houses(Houses),
	langda(LLM:"
	House arrangement:
		There are 5 houses, arranged in order (houses(Houses)).
	Rules:
		The owner of the red house is English.
		The Spanish has a dog.
		The owner of the green house drinks coffee.
		The Ukrainian drinks tea.
		The green house is to the right of the ivory house (right next to it).
		The snail owner smokes Winstons.
		The yellow house owner smokes Kools.
		The middle house drinks milk (the 3rd house).
		The first house owner is Norwegian.
		The Chesterfields owner lives next door to the fox owner.
		The Kools owner lives next door to the horse owner.
		The orange juice drinker smokes Lucky Strikes.
		The Japanese smoke Parliaments.
		The Norwegian lives next to the blue house.
		
		Someone has a zebra.
		Someone drink water.").

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

% Predicted results by DeepSeek:
% result1: zebra([house(norwegian, kools, yellow, water, fox), house(ukrainian, chesterfields, blue, tea, horse), house(english, winstons, red, milk, snail), house(spanish, lucky_strikes, ivory, orange_juice, dog), house(japanese, parliaments, green, coffee, zebra)])
result2: The Japanese person owns the zebra and the Norwegian drinks water

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is a valid Prolog implementation of the zebra puzzle, correctly structuring the problem with houses and constraints. It uses helper predicates like right_of, next_to, and my_member effectively. However, it differs from the original code in format and some details (e.g., the original uses Problog for probabilistic inference, while the generated code is pure Prolog). The results are logically consistent but presented differently: the original gives a probabilistic output, while the generated code provides deterministic solutions. Both correctly identify the Japanese person as owning the zebra and the Norwegian drinking water.
*/