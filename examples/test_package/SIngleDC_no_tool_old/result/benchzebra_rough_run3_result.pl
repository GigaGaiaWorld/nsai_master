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
right_of(X, Y, [Y,X|_]).
right_of(X, Y, [_|T]) :- right_of(X, Y, T).
query(zebra(Houses)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in terms of functionality. It successfully replicates the logic of the original zebra puzzle solution, including all constraints and member checks. The only difference is in the implementation of the 'next_to' predicate, which in the generated code is defined in terms of 'right_of', whereas the original had separate clauses. This change does not affect the behavior as 'next_to' is correctly defined to check adjacency in both directions. Both codes produce identical results, solving the puzzle with the same house arrangement.
*/