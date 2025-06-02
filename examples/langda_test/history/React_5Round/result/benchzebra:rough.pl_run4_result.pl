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
next_to(X, Y, [X,Y|_]).
next_to(X, Y, [Y,X|_]).
next_to(X, Y, [_|T]) :- next_to(X, Y, T).
right_of(X, Y, [Y,X|_]).
right_of(X, Y, [_|T]) :- right_of(X, Y, T).
query(zebra(Houses)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code. It maintains all the constraints and logic of the original zebra puzzle solution. The predicates and their implementations (my_member, next_to, right_of) are identical in functionality, just with slight variations in variable naming (e.g., 'Y' vs 'T'). The running results of both codes are exactly the same, confirming that the generated code meets the requirements.
*/