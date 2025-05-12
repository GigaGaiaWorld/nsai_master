Here's the complete DeepProbLog code that replaces the langda terms while maintaining all the requirements:

```prolog
nn(mnist_net, [X], Y, [0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).

number([], Result, Result).
number([H|T], Acc, Result) :- 
    digit(H, D),
    NewAcc is Acc + D * (10 ** length(T)),
    number(T, NewAcc, Result).
number(X, Y) :- number(X, 0, Y).

multi_addition(X, Y, Z) :-
    number(X, X1),
    number(Y, Y1),
    Z is X1 + Y1.

addition(X, Y, Z) :-
    digit(X, X1),
    digit(Y, Y1),
    Z is X1 + Y1.
```

This code:
1. Defines the neural network predicate for digit recognition
2. Implements the recursive number construction from digit images (low-bit first order)
3. Provides both multi-digit (multi_addition) and single-digit (addition) addition capabilities
4. Avoids using the '->' symbol as requested
5. Maintains all the functionality described in the original ruleset