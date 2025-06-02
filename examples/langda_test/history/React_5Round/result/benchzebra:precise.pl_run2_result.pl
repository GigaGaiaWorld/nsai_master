zebra(Houses) :-
	houses(Houses),
	

	
	% The owner of the red house is English
	my_member(house(red, english, _, _, _), Houses),
	
	% The Spanish has a dog
	my_member(house(_, spanish, _, _, dog), Houses),
	
	% The owner of the green house drinks coffee
	my_member(house(green, _, coffee, _, _), Houses),
	
	% The Ukrainian drinks tea
	my_member(house(_, ukrainian, tea, _, _), Houses),
	
	% The green house is to the right of the ivory house
	right_of(house(green, _, _, _, _), house(ivory, _, _, _, _), Houses),
	
	% The snail owner smokes Winstons
	my_member(house(_, _, _, winstons, snail), Houses),
	
	% The yellow house owner smokes Kools
	my_member(house(yellow, _, _, kools, _), Houses),
	
	% The middle house drinks milk
	Houses = [_, _, house(_, _, milk, _, _), _, _],
	
	% The first house owner is Norwegian
	Houses = [house(_, norwegian, _, _, _)|_],
	
	% The Norwegian lives next to the blue house
	next_to(house(_, norwegian, _, _, _), house(blue, _, _, _, _), Houses),
	
	% The Chesterfields owner lives next door to the fox owner
	next_to(house(_, _, _, chesterfields, _), house(_, _, _, _, fox), Houses),
	
	% The Kools owner lives next door to the horse owner
	next_to(house(_, _, _, kools, _), house(_, _, _, _, horse), Houses),
	
	% The orange juice drinker smokes Lucky Strikes
	my_member(house(_, _, orange_juice, lucky_strikes, _), Houses),
	
	% The Japanese smoke Parliaments
	my_member(house(_, japanese, _, parliaments, _), Houses),
	
	% Someone has a zebra
	my_member(house(_, _, _, _, zebra), Houses),
	
	% Someone drinks water
	my_member(house(_, _, water, _, _), Houses).
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

/* Result Report:
Validity_form: True
Validity_result: False
Report: The generated code has several issues. First, the order of attributes in the house predicate is inconsistent with the original code, leading to incorrect assignments (e.g., 'dog' is placed in the wrong position). Second, some constraints are incorrectly implemented, such as the snail owner smoking Winstons and the Chesterfields owner living next to the fox owner. These errors cause the generated code to produce a different result than the original code. Despite these issues, the generated code is syntactically valid and runs without errors.
*/