Here's the complete DeepProblog code based on the provided ruleset and requirements:

```prolog
% Neural network predicate for digit recognition
nn(mnist_net, [X], Y, [0,1,2,3,4,5,6,7,8,9]) :: digit(X, Y).

% Probabilistic fact for noise
t(0.1) :: noisy.

% Uniform distribution definition
uniform(X, Y, V) :-
    between(0, 18, V),
    P is 1/19,
    t(P).

% Noisy addition rule
addition_noisy(X, Y, Z) :-
    noisy,
    uniform(X, Y, Z).

% Correct addition rule when not noisy
addition_noisy(X, Y, Z) :-
    \+noisy,
    digit(X, N1),
    digit(Y, N2),
    Z is N1 + N2.

% Deterministic addition rule
addition(X, Y, Z) :-
    digit(X, N1),
    digit(Y, N2),
    Z is N1 + N2.
```

Key points about this implementation:
1. The `digit/2` predicate is defined using a neural network `mnist_net` that classifies input X into digits 0-9
2. The `noisy` probabilistic fact has a 10% probability of being true (t(0.1))
3. The `uniform/3` predicate generates values between 0 and 18 with equal probability (1/19)
4. The `addition_noisy/3` predicate either:
   - Returns a random uniform value when noisy is true, or
   - Performs actual digit recognition and addition when not noisy
5. The `addition/3` predicate always performs the correct digit recognition and addition

Note that I've used the `between/3` predicate to generate the uniform distribution values, which is a common Prolog idiom for such cases. The probability is set using `t(P)` where P is 1/19 for each value.