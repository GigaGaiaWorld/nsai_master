zebra(Houses) :-
    houses(Houses),
    member(house(red, english, _, _, _), Houses),        % The owner of the red house is English
    member(house(_, spanish, dog, _, _), Houses),         % The Spanish has a dog
    member(house(green, _, _, coffee, _), Houses),        % The owner of the green house drinks coffee
    member(house(_, ukrainian, _, tea, _), Houses),       % The Ukrainian drinks tea
    right_of(house(green,_,_,_,_), house(ivory,_,_,_,_), Houses), % Green is immediately to the right of ivory
    member(house(_, _, snail, _, winstons), Houses),      % The snail owner smokes Winstons
    member(house(yellow, _, _, _, kools), Houses),        % The yellow house smokes Kools
    Houses = [_,_,house(_,_,_,milk,_),_,_],              % The middle house drinks milk
    Houses = [house(_, norwegian, _, _, _)|_],           % Norwegian lives in the first house
    next_to(house(_,_,_,_,chesterfields), house(_,_,fox,_,_), Houses), % Chesterfields next to fox
    next_to(house(_,_,_,_,kools), house(_,_,horse,_,_), Houses), % Kools next to horse
    member(house(_, _, _, orange_juice, lucky_strikes), Houses), % Orange juice and Lucky Strikes
    member(house(_, japanese, _, _, parliaments), Houses), % Japanese smokes Parliaments
    next_to(house(_,norwegian,_,_,_), house(blue,_,_,_,_), Houses), % Norwegian next to blue
    member(house(_, _, zebra, _, _), Houses),             % Someone has a zebra
    member(house(_, _, _, water, _), Houses).             % Someone drinks water

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

member(X, [X|_]).
member(X, [_|Y]) :- member(X, Y).

query(zebra(Houses)).




*** Result:*** 
% Problog Inference Result：
zebra([house(yellow,norwegian,fox,water,kools), house(blue,ukrainian,horse,tea,chesterfields), house(red,english,snail,milk,winstons), house(ivory,spanish,dog,orange_juice,lucky_strikes), house(green,japanese,zebra,coffee,parliaments)]) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is largely correct and consistent with the original code. The main difference is the use of 'snail' instead of 'snails' in the generated code, which is a minor inconsistency but does not affect the logic or the result. The generated code maintains all the constraints and relationships specified in the original code, and the running results of both pieces of code are identical, indicating that the generated code meets the requirements.