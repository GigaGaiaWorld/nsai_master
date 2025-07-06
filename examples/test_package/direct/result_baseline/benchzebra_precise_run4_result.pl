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
% result1: zebra([house(norwegian, yellow, kools, water, fox), house(ukrainian, blue, chesterfields, tea, horse), house(english, red, winstons, milk, snail), house(spanish, ivory, lucky_strikes, orange_juice, dog), house(japanese, green, parliaments, coffee, zebra)])
result2: The Japanese owns the zebra and the Norwegian drinks water

/* Result Report:
Validity_form: True
Validity_result: False
Report: The generated code is a valid Prolog implementation of the zebra puzzle, correctly structuring the problem with houses and constraints. It uses predicates like `right_of`, `next_to`, and `my_member` to enforce the puzzle rules. However, the generated code does not include the actual constraint-solving logic, relying instead on an LLM to interpret the rules. The original code provides a concrete solution with probabilities, while the generated code only outlines the problem structure and hints at a solution. The results are conceptually consistent but differ in presentation and completeness.
*/