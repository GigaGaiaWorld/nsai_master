Based on the requirements and the given ruleset, I'll generate the Problog code to replace the `langda` term. Here's the complete implementation:

```prolog
wap(Text,X1,X2,X3,Out) :-
    rnn(Text,Embedding),
    net1(Embedding,Permute),
    permute(Permute,X1,X2,X3,A,B,C),
    net3(Embedding,Swap),
    swap(Swap,A,B,D,E),
    min(D,E,Min1),
    max(D,E,Max1),
    Min2 is min(Max1,C),
    Max2 is max(Max1,C),
    net2(Embedding,Op1),
    operator(Op1,Min1,Min2,Sum),
    net4(Embedding,Op2),
    operator(Op2,Sum,Max2,Out).
```

This implementation:
1. Takes the text embedding from the RNN
2. Uses net1 to determine the permutation of the three numbers
3. Uses net3 to determine whether to swap the first two numbers
4. Finds the two smallest numbers (Min1 and Min2) and the largest number (Max2)
5. Uses net2 to determine the operation for adding the two smallest numbers
6. Uses net4 to determine the operation for subtracting the largest number from the sum
7. Returns the final result (Out)

The code follows the requirement of "adding the smallest two numbers and then subtracting the largest" while using all the neural networks (net1, net2, net3, net4) as specified in the original ruleset.