Here's the complete DeepProblog code based on your requirements:

```prolog
% Neural network predicate for digit recognition
nn(mnist_net, [X], Y, [0,1,2,3,4,5,6,7,8,9]) :: digit(X, Y).

% Addition rule that sums the recognized digits
addition(X, Y, Z) :- 
    digit(X, X2), 
    digit(Y, Y2), 
    Z is X2 + Y2.

% Rule to calculate the sum of all numbers in a list
anysum(Bag, R) :-
    anysum_helper(Bag, 0, R).

% Helper predicate for anysum using accumulator
anysum_helper([], Acc, Acc).
anysum_helper([H|T], Acc, R) :-
    digit(H, Digit),
    NewAcc is Acc + Digit,
    anysum_helper(T, NewAcc, R).
```

Notes:
1. I've implemented `anysum` using a helper predicate with an accumulator, which is a standard Prolog pattern for summing list elements.
2. The implementation doesn't use the `->` symbol as requested.
3. Each element in the Bag is passed through the digit recognizer before being summed.
4. The code maintains all the functionality from your original ruleset while being properly structured.