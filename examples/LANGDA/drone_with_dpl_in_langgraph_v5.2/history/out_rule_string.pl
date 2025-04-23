
% =============================== % EXAMPLE % =============================== %
% UAV properties
initial_langda_content[i]ge ~ normal(90, 5).
langda_content[i]ge_cost ~ normal(-0.1, 0.2).
weight ~ normal(0.2, 0.1).

% Weather conditions
1/10::fog; 9/10::clear.

% Visual line of sight
vlos(X) :- 
    fog, distance(X, operator) < 50;
    clear, distance(X, operator) < 100;
    clear, over(X, bay), distance(X, operator) < 400.

% []% [[LANGDA]]
langda(ans).
% langda(X:"answer",LLM).
% 
% ---------------------------- Network and Event Predicates ---------------------------- %
% NN Predicates:
nn(mlp, [X], Y, [1, 2, 3, 4, 5, 6]) :: mlp(X, Y).

% Event Predicate:
event(ID1, T) :-
    happenAt(X, T),
    mlp(X, ID1).
% [[LANGDA]]
langda(why).
% []% [[LANGDA]]
langda(X).

% Sufficient langda_content[i]ge to return to operator
can_return(X) :- 
    B is initial_langda_content[i]ge, O is langda_content[i]ge_cost,
    D is distance(X, operator), 0 < B + (2 * O * D).

% Permits related to local features
permits(X) :- 
    distance(X, service) < 15; distance(X, primary) < 15;
    distance(X, secondary) < 10; distance(X, tertiary) < 5;
    distance(X, crossing) < 5; distance(X, rail) < 5;
    over(X, park).

% 
% ---------------------------- Network and Event Predicates ---------------------------- %
% NN Predicates:
nn(mnist_net1, [X], Y, [0, 1]) :: mnist_net1(X, Y).
nn(mnist_net2, [X], Y, [2, 3]) :: mnist_net2(X, Y).

% Event Predicate:
event(ID1, ID2, T) :-
    happenAt(X, Y, T),
    mnist_net1(X, ID1),
    mnist_net2(Y, ID2).
% [[LANGDA]]
valid_drone_flight(X) :- (langda(X,T), vlos(X));(can_return(X));langda(T).

% 
% ---------------------------- Network and Event Predicates ---------------------------- %
% NN Predicates:
nn(mnist_net1, [X], Y, [0, 1]) :: mnist_net1(X, Y).
nn(mnist_net2, [X], Y, [2, 3]) :: mnist_net2(X, Y).

% Event Predicate:
event(ID1, ID2, T) :-
    happenAt(X, Y, T),
    mnist_net1(X, ID1),
    mnist_net2(Y, ID2).
% [[LANGDA]]
coin_win() :-
    langda(X,T), 
    permits(X), langda(X,Y,Z).
    
% Definition of a valid mission
landscape(X) :- 
    vlos(X), weight < 25, can_return(X); 
    permits(X), can_return(X).
