Here's the complete DeepProbLog code based on the provided ruleset and requirements:

```prolog
% Neural network declarations
nn(neural1, [I1, I2, Carry], O, [0,1,2,3,4,5,6,7,8,9]) :: result(I1, I2, Carry, O).
nn(neural2, [I1, I2, Carry], NewCarry, [0,1]) :: carry(I1, I2, Carry, NewCarry).

% Slot predicate that encapsulates the addition operation
slot(I1, I2, Carry, Carry2, O) :-
    result(I1, I2, Carry, O),
    carry(I1, I2, Carry, Carry2).

% Base case for addition - empty lists
add([], [], C, C, []).

% Recursive case for addition - process digits
add([H1|T1], [H2|T2], C, Carry, [Digit|Res]) :-
    add(T1, T2, C, Carry2, Res),
    slot(H1, H2, Carry2, Carry, Digit).

% Wrapper predicate that includes the final carry
add(L1, L2, C, [Carry|Res]) :- 
    add(L1, L2, C, Carry, Res).
```

Key points about this implementation:
1. The neural networks `neural1` and `neural2` are declared to handle digit results and carry values respectively
2. The `slot` predicate combines both neural networks to perform a single digit addition with carry
3. The `add` predicates implement recursive addition of digit lists:
   - The base case handles empty lists
   - The recursive case processes each digit pair
   - The wrapper adds the final carry to the result
4. The code avoids using the '->' symbol as requested
5. The commented alternative versions from the original are not included since they weren't part of the requirements

The code maintains all the functionality described in the original ruleset while being properly formatted for DeepProbLog.