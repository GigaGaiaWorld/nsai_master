% UAV properties
initial_charge ~ normal(90, 5).
charge_cost ~ normal(-0.1, 0.2).
weight ~ normal(0.2, 0.1).
% Weather conditions
1/10::fog; 9/10::clear.
% Visual line of sight
vlos(X) :-
fog, distance(X, operator) < 50;
clear, distance(X, operator) < 100;
clear, over(X, bay), distance(X, operator) < 400.
% Sufficient charge to return to operator
can_return(X) :-

% === % LLM Generated Logic Codes % === %
initial_charge(B), charge_cost(O), distance(X, operator, D), B + 2 * O * D > 0.

% === % ========================= % === %

% Permits related to local features
permits(X) :-
distance(X, service) < 15; distance(X, primary) < 15;
distance(X, secondary) < 10; distance(X, tertiary) < 5;
distance(X, crossing) < 5; distance(X, rail) < 5;
over(X, park).
% Definition of a valid mission
landscape(X) :-
vlos(X), weight < 25, can_return(X);
permits(X), can_return(X).