% UAV properties
initial_charge ~ normal(90, 5).
charge_cost ~ normal(-0.1, 0.2).
weight ~ normal(0.2, 0.1).

% Weather conditions
1/10::fog; 9/10::clear.


langda(LLM:"we found a bomb on the map, please stay 100 meters away from it",FUP:"F").

% Visual line of sight
vlos(X) :- 
    fog, distance(X, operator) < 50;
    clear, distance(X, operator) < 100;
    clear, over(X, bay), distance(X, operator) < 400.

% Sufficient charge to return to operator
can_return(X) :-
    B is initial_charge, O is charge_cost,
    D is distance(X, operator), 0 < B + (2 * O * D).

% Definition of a valid mission
landscape(X) :- 
    langda(LLM:"If the drone meets one of the following conditions, the mission will be allowed to be carried out: 
        1.visual route range + light weight + returnable
        2.permission obtained + returnable
        # Additionally, it should not violate the requirements of other langda predicates.
    ",FUP:"T").

% Permits related to local features
permits(X) :- 
    distance(X, service) < 15; distance(X, primary) < 15;
    distance(X, secondary) < 10; distance(X, tertiary) < 5;
    distance(X, crossing) < 5; distance(X, rail) < 5;
    over(X, park).

