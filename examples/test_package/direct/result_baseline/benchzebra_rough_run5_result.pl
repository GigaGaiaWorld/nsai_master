zebra(Houses) :-
	houses(Houses),
	my_member(house(red, english, _, _, _), Houses),
	my_member(house(_, spanish, dog, _, _), Houses),
	my_member(house(green, _, _, coffee, _), Houses),
	my_member(house(_, ukrainian, _, tea, _), Houses),
	right_of(house(green,_,_,_,_), house(ivory,_,_,_,_), Houses),
	my_member(house(_, _, snails, _, winstons), Houses),
	my_member(house(yellow, _, _, _, kools), Houses),
	Houses = [_, _, house(_, _, _, milk, _), _,_],
	Houses = [house(_, norwegian, _, _, _)|_],
	next_to(house(_,_,_,_,chesterfields), house(_,_,fox,_,_), Houses),
	next_to(house(_,_,_,_,kools), house(_,_,horse,_,_), Houses),
	my_member(house(_, _, _, orange_juice, lucky_strikes), Houses),
	my_member(house(_, japanese, _, _, parliaments), Houses),
	next_to(house(_,norwegian,_,_,_), house(blue,_,_,_,_), Houses),
	my_member(house(_, _, zebra, _, _), Houses),
	my_member(house(_, _, _, water, _), Houses).

houses([
	house(_, _, _, _, _),
	house(_, _, _, _, _),
	house(_, _, _, _, _),
	house(_, _, _, _, _),
	house(_, _, _, _, _)
]).

langda(LLM:"define the my_member/2 predicate.").
langda(LLM:"define the next_to/3 predicate.").
langda(LLM:"define the right_of/3 predicate.").

query(zebra(Houses)).

% Predicted results by DeepSeek:
% result1: zebra([house(yellow, norwegian, fox, water, kools), house(blue, ukrainian, horse, tea, chesterfields), house(red, english, snails, milk, winstons), house(ivory, spanish, dog, orange_juice, lucky_strikes), house(green, japanese, zebra, coffee, parliaments)])
result2: The Japanese person owns the zebra, and the Norwegian drinks water.

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is a valid Prolog implementation of the zebra puzzle, correctly defining the constraints and relationships between the houses. It includes necessary predicates like my_member/2, next_to/3, and right_of/3, though their definitions are not shown. The generated code's result matches the original code's output, confirming that the Japanese person owns the zebra and the Norwegian drinks water. Both codes produce consistent results, indicating correctness in logic and implementation.
*/