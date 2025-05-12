Here's the complete DeepProblog code implementing bit-by-bit addition of two numbers based on your requirements:

```prolog
% Neural network declarations
nn(neural1, [I1, I2, Carry], O, [0,1,2,3,4,5,6,7,8,9]) :: result(I1, I2, Carry, O).
nn(neural2, [I1, I2, Carry], NewCarry, [0,1]) :: carry(I1, I2, Carry, NewCarry).

% Slot relation combining result and carry
slot(I1, I2, Carry, Carry2, O) :-
    result(I1, I2, Carry, O),
    carry(I1, I2, Carry, Carry2).

% Main addition predicate
add_numbers(L1, L2, C0, Result) :-
    add_digits(L1, L2, C0, [], Result).

% Base case when both lists are empty - add final carry if needed
add_digits([], [], Carry, Acc, FinalResult) :-
    (Carry =:= 0 -> 
        FinalResult = Acc
    ; 
        reverse([Carry|Acc], FinalResult)
    ).

% Recursive case for adding digits
add_digits([D1|T1], [D2|T2], CurrentCarry, Acc, Result) :-
    slot(D1, D2, CurrentCarry, NewCarry, SumDigit),
    add_digits(T1, T2, NewCarry, [SumDigit|Acc], Result).

% Example usage
% To add 347 + 568:
% L1 = [7,4,3], L2 = [8,6,5], C0 = 0
% Expected result: [5,1,9,0] (which represents 0915 or 915)
```

This code implements:

1. Two neural networks:
   - `neural1` predicts the result digit (0-9) given two input digits and a carry
   - `neural2` predicts the new carry (0 or 1) given two input digits and a carry

2. A `slot` predicate that combines the results from both neural networks

3. The main addition logic:
   - `add_numbers/4` is the entry point that takes two digit lists (in reverse order) and initial carry
   - `add_digits/5` recursively processes each digit pair:
     - Uses the neural networks to get sum digit and new carry
     - Accumulates results
     - Handles the final carry if needed

4. The example shows how to represent 347 + 568 as [7,4,3] + [8,6,5] with initial carry 0, which should produce [5,1,9,0] (representing 915).

The code follows the exact processing steps described in your requirements, performing bit-by-bit addition with carry propagation.