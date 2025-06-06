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
next_to(X, Y, List) :- append(_, [X,Y|_], List).
next_to(X, Y, List) :- append(_, [Y,X|_], List).
right_of(X, Y, List) :- append(_, [Y,X|_], List).
query(zebra(Houses)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code is mostly consistent with the original code in terms of logic and structure. However, it introduces a critical error by using 'append/3' without defining or importing it, leading to a runtime error. The original code uses custom definitions for 'next_to' and 'right_of', which work correctly. The generated code's attempt to simplify these predicates with 'append/3' fails because 'append/3' is not available in the Problog environment used.
*/