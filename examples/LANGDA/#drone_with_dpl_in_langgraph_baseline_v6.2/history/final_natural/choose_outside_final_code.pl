Here's the complete DeepProblog code that captures all the requirements from the ruleset:

```prolog
nn(neural1,[I1,I2,Carry],O,[0,1,2,3,4,5,6,7,8,9]) :: result(I1,I2,Carry,O).
nn(neural2,[I1,I2,Carry],NewCarry,[0,1]) :: carry(I1,I2,Carry,NewCarry).

slot(I1,I2,Carry,Carry2,O) :-
    result(I1,I2,Carry,O),
    carry(I1,I2,Carry,Carry2).

add([],[],C,C,[]).
add([H1|T1],[H2|T2],C,Carry,[Digit|Res]) :-
    slot(H1,H2,C,NewCarry,Digit),
    add(T1,T2,NewCarry,Carry,Res).
```

This code:
1. Maintains the neural network declarations for `neural1` and `neural2`
2. Keeps the `slot` predicate that combines the results from both networks
3. Implements the complete `add/5` predicate with recursive logic for multi-digit addition
4. Handles the base case (empty lists) and recursive case for lists with heads and tails
5. Uses the `slot` predicate to compute each digit and carry in the addition process

The code follows all the requirements and doesn't use the '->' symbol. It should properly handle the addition of numbers represented as lists of digits.