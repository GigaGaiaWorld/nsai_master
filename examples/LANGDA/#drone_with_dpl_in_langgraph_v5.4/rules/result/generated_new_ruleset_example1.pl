
initial_charge ~ normal(90, 5).
charge_cost ~ normal(-0.1, 0.2).
weight ~ normal(0.2, 0.1).
1/10::fog; 9/10::clear.
vlos(X) :-
fog, distance(X, operator) < 50;
clear, distance(X, operator) < 100;
clear, over(X, bay), distance(X, operator) < 400.
can_return(X) :-
B is initial_charge, O is charge_cost,
D is distance(X, operator), 0 < B + (2 * O * D).
permits(X) :-

% ---------------------------- LLM Generated Logic Codes ------------------------------- %
distance(X, service) < 20;

distance(X, primary) < 15;
distance(X, secondary) < 10; distance(X, tertiary) < 5;
distance(X, crossing) < 5; distance(X, rail) < 5;
over(X, park).
landscape(X) :-
vlos(X), weight < 25, can_return(X);
permits(X), can_return(X).