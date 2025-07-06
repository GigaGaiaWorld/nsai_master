zebra(Houses) :-
	houses(Houses),
	
my_member(house(english, red, _, _, _), Houses)
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
/* %%% Result %%% 
% Problog Inference Result：
zebra([house(english,red,X33,X34,X35), house(X36,X37,X38,X39,X40), house(X41,X42,X43,X44,X45), house(X46,X47,X48,X49,X50), house(X51,X52,X53,X54,X55)]) = 1.0000
zebra([house(X36,X37,X38,X39,X40), house(english,red,X33,X34,X35), house(X41,X42,X43,X44,X45), house(X46,X47,X48,X49,X50), house(X51,X52,X53,X54,X55)]) = 1.0000
zebra([house(X36,X37,X38,X39,X40), house(X41,X42,X43,X44,X45), house(english,red,X33,X34,X35), house(X46,X47,X48,X49,X50), house(X51,X52,X53,X54,X55)]) = 1.0000
zebra([house(X36,X37,X38,X39,X40), house(X41,X42,X43,X44,X45), house(X46,X47,X48,X49,X50), house(english,red,X33,X34,X35), house(X51,X52,X53,X54,X55)]) = 1.0000
zebra([house(X36,X37,X38,X39,X40), house(X41,X42,X43,X44,X45), house(X46,X47,X48,X49,X50), house(X51,X52,X53,X54,X55), house(english,red,X33,X34,X35)]) = 1.0000
*/