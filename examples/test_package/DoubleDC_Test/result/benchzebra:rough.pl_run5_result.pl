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
my_member(X, [X|_]).
my_member(X, [_|T]) :- my_member(X, T).
next_to(X, Y, List) :- right_of(X, Y, List).
next_to(X, Y, List) :- right_of(Y, X, List).
right_of(X, Y, [Y, X|_]).
right_of(X, Y, [_|T]) :- right_of(X, Y, T).
query(zebra(Houses)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in terms of functionality and logic. It successfully solves the zebra puzzle with the same constraints and produces identical results. The only differences are in the organization of helper predicates (my_member, next_to, right_of), which are equivalently defined but slightly rearranged. This does not affect the program's behavior or outcome.
*/