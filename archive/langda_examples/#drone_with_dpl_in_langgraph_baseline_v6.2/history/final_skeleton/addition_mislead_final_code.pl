Here's the complete DeepProbLog code based on the provided ruleset and requirements:

```prolog
% Import necessary modules
:- use_module(library(deepproblog)).
:- use_module(library(lists)).

% Define the neural network model
nn(mnist_net, [X], Y, [0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).

% Base case for number/3: empty list returns accumulated result
number([], Result, Result).

% Recursive case for number/3: process each digit image
number([H|T], Acc, Result) :-
    digit(H, D),          % Recognize the digit using MNIST network
    NewAcc is Acc + (D * (10 ^ length(T))),  % Update accumulator
    number(T, NewAcc, Result).  % Recurse with tail

% Wrapper for number/2 that starts with accumulator 0
number(X, Y) :- number(X, 0, Y).

% multi_addition predicate: converts two digit sequences to numbers and adds them
multi_addition(X, Y, Z) :-
    number(X, X1),       % Convert first sequence to number
    number(Y, Y1),       % Convert second sequence to number
    Z is X1 + Y1.        % Compute sum

% addition predicate: adds two single-digit numbers from images
addition(X, Y, Z) :-
    digit(X, X1),        % Recognize first digit
    digit(Y, Y2),        % Recognize second digit
    Z is X1 + Y2.        % Compute sum
```

Key points about this implementation:
1. The `digit/2` predicate uses the MNIST network to recognize digits from images
2. `number/3` recursively processes lists of digit images to form multi-digit numbers (in little-endian order)
3. `number/2` is a convenience wrapper that starts the accumulation with 0
4. `multi_addition/3` handles multi-digit addition by first converting image sequences to numbers
5. `addition/3` handles single-digit addition directly from images
6. All neural network operations are properly integrated with the logical reasoning

The code avoids using the '->' symbol as requested and maintains all the functionality described in the original ruleset.