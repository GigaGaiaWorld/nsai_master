Here's the complete DeepProbLog code that replaces the langda terms while maintaining all the original functionality:

```prolog
digit(X,Y) :: mnist_net("mnist network", [X], Y, [0,1,2,3,4,5,6,7,8,9]).

addition(X,Y,Z) :-
    digit(X,A),
    digit(Y,B),
    Z is A + B.
```

This code:
1. Defines the `digit/2` predicate using the mnist_net neural network with 10 possible output digits (0-9)
2. Implements the addition predicate by:
   - First recognizing digit A from image X
   - Then recognizing digit B from image Y
   - Finally calculating their sum Z

The code maintains all the original requirements without using the '->' symbol and replaces the natural language specifications with proper DeepProbLog syntax.