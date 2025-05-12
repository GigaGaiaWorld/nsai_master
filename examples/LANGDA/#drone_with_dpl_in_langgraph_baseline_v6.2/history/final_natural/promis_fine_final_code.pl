Here's the complete DeepProbLog code that replaces the langda terms while maintaining all the original requirements:

```prolog
% UAV properties
initial_charge ~ normal(90, 5).
charge_cost ~ normal(-0.1, 0.2).
weight ~ normal(0.2, 0.1).

% Weather conditions
1/10::fog; 9/10::clear.

% Bomb constraint
:- distance(X, bomb) < 100.

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
    (permits(X), can_return(X)).

% Permits related to local features
permits(X) :-
    distance(X, service) < 15; distance(X, primary) < 15;
    distance(X, secondary) < 10; distance(X, tertiary) < 5;
    distance(X, crossing) < 5; distance(X, rail) < 5;
    over(X, park).
```

Key changes made:
1. Replaced the bomb warning with a constraint `:- distance(X, bomb) < 100.`
2. Translated the landscape conditions into proper Prolog syntax with two alternatives:
   - Visual route range + light weight + returnable
   - Permission obtained + returnable
3. Maintained all other original rules exactly as specified
4. Avoided using the '->' symbol as requested