Here's the complete DeepProbLog code based on the provided ruleset and requirements:

```prolog
% Neural network predicate for digit recognition
nn(mnist_net, [X], Y, [0,1,2,3,4,5,6,7,8,9]) :: digit(X, Y).

% Addition rule that sums the recognized digits
addition(X, Y, Z) :- 
    digit(X, X2), 
    digit(Y, Y2), 
    Z is X2 + Y2.

% Rule for calculating sum using a language model
anysum(Bag, R) :- 
    langda(LLM:"Calculate the sum of numbers.").
```

This code includes:
1. The digit recognition neural network predicate that takes an image X and outputs a digit Y between 0-9
2. The addition rule that takes two images, recognizes their digits, and sums them
3. The anysum rule that uses a language model to calculate sums

The code avoids using the '->' symbol as requested and maintains all the functionality from the original ruleset.