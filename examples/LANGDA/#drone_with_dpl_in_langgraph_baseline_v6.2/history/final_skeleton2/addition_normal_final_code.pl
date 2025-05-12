Here's the complete DeepProbLog code that replaces the `langda` terms while maintaining all the specified functionality:

```prolog
digit(X,Y) :: mnist_net("mnist network", [X], Y, [0,1,2,3,4,5,6,7,8,9]).

number([], Result, Result).
number([H|T], Acc, Result) :- 
    digit(H, D),
    NewAcc is Acc + (D * (10 ^ length(T))),
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

Explanation:
1. The `digit` predicate uses the neural network `mnist_net` to classify an image into one of the digits 0-9.
2. The `number` predicates recursively process a list of digit images to construct a multi-digit number (in low-bit first order).
3. The `multi_addition` predicate converts two sequences of digit images into numbers and adds them.
4. The `addition` predicate identifies digits in two images and calculates their sum.

The code follows all requirements and avoids using the '->' symbol.