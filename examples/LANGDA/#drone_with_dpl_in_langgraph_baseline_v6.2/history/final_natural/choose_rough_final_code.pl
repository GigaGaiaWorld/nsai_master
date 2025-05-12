Here's the complete DeepProbLog code that implements bit-by-bit addition of two numbers, following the given requirements and without using the '->' symbol:

```prolog
nn(neural1,[I1,I2,Carry],O,[0,1,2,3,4,5,6,7,8,9]) :: result(I1,I2,Carry,O).
nn(neural2,[I1,I2,Carry],NewCarry,[0,1]) :: carry(I1,I2,Carry,NewCarry).

slot(I1,I2,Carry,Carry2,O) :-
    result(I1,I2,Carry,O),
    carry(I1,I2,Carry,Carry2).
```

This code:
1. Defines two neural networks (neural1 and neural2) with their respective input/output specifications
2. neural1 predicts the result digit (0-9) given two input digits and a carry
3. neural2 predicts the new carry (0 or 1) given two input digits and a carry
4. Defines a slot/5 predicate that combines both neural networks to perform the bit-by-bit addition
5. The commented alternative versions and one-hot encoding implementations have been removed as they weren't part of the core requirements

The code maintains all the functionality described in the original ruleset while being more concise and following ProbLog syntax conventions.