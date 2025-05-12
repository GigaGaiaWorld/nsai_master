Here's the complete Problog code with the `langda` terms replaced by their corresponding Problog rules:

```prolog
% UAV properties
initial_charge ~ normal(90, 5).
charge_cost ~ normal(-0.1, 0.2).
weight ~ normal(0.2, 0.1).

% Weather conditions
1/10::fog; 9/10::clear.

% Bomb safety constraint
mission_allowed(X) :- distance(X, bomb) >= 100.

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
    (vlos(X), weight < 0.3, can_return(X));
    (permits(X), can_return(X)),
    mission_allowed(X).

% Permits related to local features
permits(X) :- 
    distance(X, service) < 15; distance(X, primary) < 15;
    distance(X, secondary) < 10; distance(X, tertiary) < 5;
    distance(X, crossing) < 5; distance(X, rail) < 5;
    over(X, park).
```

Key changes made:
1. Replaced the bomb safety `langda` term with a direct rule `mission_allowed(X) :- distance(X, bomb) >= 100.`
2. Replaced the mission conditions `langda` term with explicit rules in the `landscape` predicate that check:
   - Visual line of sight + light weight + return capability, OR
   - Permission obtained + return capability
   - Plus the bomb safety constraint
3. Maintained all other existing rules exactly as they were
4. Followed the requirement to not use the '->' symbol