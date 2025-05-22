Here's the complete DeepProbLog code based on the provided ruleset and requirements:

```prolog
% Neural network declarations
nn(rnn, [Text], Embedding, []) :: rnn(Text, Embedding).
nn(nn_permute, [X], Y, [0,1,2,3,4,5]) :: net1(X, Y).
nn(nn_op1, [X], Y, [plus,minus,times,div]) :: net2(X, Y).
nn(nn_swap, [X], Y, [no_swap,swap]) :: net3(X, Y).
nn(nn_op2, [X], Y, [plus,minus,times,div]) :: net4(X, Y).

% Permutation rules
permute(0, A, B, C, A, B, C).
permute(1, A, B, C, A, C, B).
permute(2, A, B, C, B, A, C).
permute(3, A, B, C, B, C, A).
permute(4, A, B, C, C, A, B).
permute(5, A, B, C, C, B, A).

% Swap rules
swap(no_swap, X, Y, X, Y).
swap(swap, X, Y, Y, X).

% Operator definitions
operator(plus, X, Y, Z) :- Z is X + Y.
operator(minus, X, Y, Z) :- Z is X - Y.
operator(times, X, Y, Z) :- Z is X * Y.
operator(div, X, Y, Z) :- Y > 0, 0 =:= X mod Y, Z is X // Y.

% Main wap predicate
wap(Text, X1, X2, X3, Out) :-
    rnn(Text, Embedding),
    net1(Embedding, Perm),
    net2(Embedding, Op1),
    net3(Embedding, Swap),
    net4(Embedding, Op2),
    permute(Perm, X1, X2, X3, A, B, C),
    operator(Op1, A, B, Temp),
    swap(Swap, Temp, C, D, E),
    operator(Op2, D, E, Out).
```

This code includes:
1. All the neural network declarations with their respective input/output types
2. The permutation rules for reordering three numbers
3. The swap rules for optionally swapping two numbers
4. The arithmetic operator definitions
5. The main `wap` predicate that:
   - Uses the RNN to get an embedding from text
   - Uses all four neural networks to predict operations
   - Applies the permutation to the input numbers
   - Performs the first operation
   - Optionally swaps the result with the third number
   - Performs the final operation to get the output

The implementation follows the requirement to "Add the smallest two numbers and then subtract the largest" through the neural network predictions and the operation sequence.