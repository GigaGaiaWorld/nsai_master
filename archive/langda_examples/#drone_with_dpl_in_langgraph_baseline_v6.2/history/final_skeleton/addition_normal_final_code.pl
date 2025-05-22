Here's the complete DeepProbLog code based on the provided ruleset and requirements:

```prolog
% Import necessary modules
:- use_module(library(deepproblog)).

% Define the neural network model
network(mnist_net).
mnist_net("mnist network", [X], Y, [0,1,2,3,4,5,6,7,8,9]) :: digit(X, Y).

% Base case for number/3: empty list returns accumulated result
number([], Result, Result).

% Recursive case for number/3: process each digit image and build the number
number([H|T], Acc, Result) :-
    digit(H, D),
    NewAcc is Acc + (D * (10 ^ length(T))),
    number(T, NewAcc, Result).

% Wrapper for number/2 that initializes the accumulator
number(X, Y) :- number(X, 0, Y).

% Multi-digit addition by converting image sequences to numbers first
multi_addition(X, Y, Z) :-
    number(X, XNum),
    number(Y, YNum),
    Z is XNum + YNum.

% Single-digit addition directly using neural network predictions
addition(X, Y, Z) :-
    digit(X, XD),
    digit(Y, YD),
    Z is XD + YD.
```

Key points about this implementation:
1. The `digit/2` predicate uses the MNIST network to classify individual digit images
2. `number/3` recursively processes a list of digit images to construct a multi-digit number
3. The number is constructed in low-bit first order (right-to-left)
4. `multi_addition/3` handles multi-digit addition by first converting image sequences to numbers
5. `addition/3` handles single-digit addition directly using neural network predictions
6. All arithmetic operations are performed using standard Prolog arithmetic

The code avoids using the '->' symbol as requested and implements all the specified functionality from the natural language description.