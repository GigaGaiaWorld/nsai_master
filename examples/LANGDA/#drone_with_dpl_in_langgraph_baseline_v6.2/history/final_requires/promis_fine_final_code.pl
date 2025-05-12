Here's the complete code with the placeholders filled according to the requirements:

```prolog
% UAV properties
initial_charge ~ normal(90, 5).
charge_cost ~ normal(-0.1, 0.2).
weight ~ normal(0.2, 0.1).
% Weather conditions
1/10::fog; 9/10::clear.
distance(X, bomb) >= 100.
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

Key points about the generated code:
1. For the first placeholder (3BCDB921), I added `distance(X, bomb) >= 100.` to ensure the drone stays 100 meters away from the bomb.
2. For the second placeholder (C5CAAC05), I implemented the two conditions for a valid mission:
   - `(vlos(X), weight < 0.3, can_return(X))` for visual route range + light weight + returnable
   - `(permits(X), can_return(X))` for permission obtained + returnable
3. The code maintains proper Problog syntax without using the '->' symbol as requested.
4. All original rules are preserved exactly as they were, with only the placeholders filled in.