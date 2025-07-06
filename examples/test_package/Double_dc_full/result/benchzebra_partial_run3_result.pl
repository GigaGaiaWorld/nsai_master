zebra(Houses) :-
	houses(Houses),
	
my_member(house(red, english, _, _, _), Houses)
,
	
my_member(house(_, spanish, dog, _, _), Houses)
,
	
my_member(house(green, _, _, coffee, _), Houses)
,
	my_member(house(_, ukrainian, _, tea, _), Houses),
	right_of(house(green,_,_,_,_), house(ivory,_,_,_,_), Houses),
	
my_member(house(_, _, snail, _, winstons), Houses)
,
	my_member(house(yellow, _, _, _, kools), Houses),
	
Houses = [_, _, house(_, _, _, milk, _), _, _]
,
	Houses = [house(_, norwegian, _, _, _)|_],
	next_to(house(_,_,_,_,chesterfields), house(_,_,fox,_,_), Houses),
	next_to(house(_,_,_,_,kools), house(_,_,horse,_,_), Houses),
	my_member(house(_, _, _, orange_juice, lucky_strikes), Houses),
	my_member(house(_, japanese, _, _, parliaments), Houses),
	
next_to(house(_, norwegian, _, _, _), house(blue, _, _, _, _), Houses)
,
	
my_member(house(_, _, zebra, _, _), Houses)
,
	
my_member(house(_, _, _, water, _), Houses)
.
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
Validity_result: True
Report: The generated code is mostly consistent with the original code, but there is a minor typographical error where 'snails' is written as 'snail' in the generated code. Despite this, the running results of both codes are consistent, producing the same output. The generated code maintains the same logical structure and constraints as the original, making it functionally equivalent except for the typo.
*/