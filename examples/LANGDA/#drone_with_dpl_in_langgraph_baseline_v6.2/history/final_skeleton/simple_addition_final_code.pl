Here's the complete DeepProbLog code based on the given ruleset and requirements:

```problog
% Neural network declaration for MNIST digit recognition
nn(mnist_net, [X], Y, [0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).

% Language model annotation declaration
langda(LLM:"", FUP:"False").

% Addition rule using neural network for digit recognition
addition(X, Y, Z) :-
    langda(NET:"use mnist network", 
           LLM:"Use a neural network to identify the numbers in two pictures and then calculate their sum."),
    digit(X, X_val),
    digit(Y, Y_val),
    Z is X_val + Y_val.
```

This code includes:
1. The neural network declaration for MNIST digit recognition with 10 possible outputs (0-9)
2. The langda predicate declaration with empty LLM and False FUP parameters
3. The addition rule that:
   - Uses the langda annotation specifying to use the MNIST network
   - Calls the digit predicate on both input images to get their values
   - Calculates the sum of the recognized digits

The code avoids using the '->' symbol as requested.