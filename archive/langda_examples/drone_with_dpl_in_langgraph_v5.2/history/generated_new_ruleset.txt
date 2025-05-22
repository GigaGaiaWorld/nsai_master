
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

% []% % ---------------------------- LLM Generated Logic Codes ------------------------------- %
% Simple answer predicate
langda(ans).

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
% % ---------------------------- LLM Generated Logic Codes ------------------------------- %
% Why predicate with neural network definition
langda(why) :-
    mlp(_, why, [1,2,3,4,5,6]).

langda(why).
% []% % ---------------------------- LLM Generated Logic Codes ------------------------------- %
% Unknown variable predicate
langda(X).

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
% % ---------------------------- LLM Generated Logic Codes ------------------------------- %
% Valid drone flight with neural networks and LLM information
valid_drone_flight(X) :-
    (langda(X,T), vlos(X));
    (can_return(X));
    langda(T).

langda(Return, Unknown) :-
    mnist_net1(_, 0),
    mnist_net2(_, 2),
    % LLM information: there's a high building at: (100,200)
    building_at(100,200).

langda(anstimewer).

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
% % ---------------------------- LLM Generated Logic Codes ------------------------------- %
% Coin win predicate with complex conditions
coin_win() :-
    langda(return, time),
    permits(return),
    langda(return, fun, darmstadt).

langda(return, time) :-
    mnist_net1(_, 1),
    mnist_net2(_, 3),
    % LLM information: If the code difference is 2, it returns 1, otherwise it returns 0.
    (code_diff(2) -> returns(1); returns(0)).

langda(return, fun, darmstadt) :-
    position_net(there, here),
    audio(dog, child, horn),
    % LLM information: If the we is 2, and horn is there, we eat banana.
    (we(2), horn(there) -> eat(banana).

coin_win() :-
    langda(X,T), 
    permits(X), langda(X,Y,Z).
    
% Definition of a valid mission
landscape(X) :- 
    vlos(X), weight < 25, can_return(X); 
    permits(X), can_return(X).
