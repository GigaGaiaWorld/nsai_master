Here's the complete DeepProbLog code that implements bit-by-bit addition of two numbers according to the given requirements:

```prolog
nn(neural1,[I1,I2,Carry],O,[0,1,2,3,4,5,6,7,8,9]) :: result(I1,I2,Carry,O).
nn(neural2,[I1,I2,Carry],NewCarry,[0,1]) :: carry(I1,I2,Carry,NewCarry).

slot(I1,I2,Carry,Carry2,O) :-
    result(I1,I2,Carry,O),
    carry(I1,I2,Carry,Carry2).

add_numbers([],[],Carry,[Carry]) :- Carry > 0.
add_numbers([],[],0,[]).
add_numbers([H1|T1],[H2|T2],CarryIn,[Res|Rest]) :-
    slot(H1,H2,CarryIn,NewCarry,Res),
    add_numbers(T1,T2,NewCarry,Rest).

% Example query:
% add_numbers([7,4,3],[8,6,5],0,Result).
% Result = [5,1,9,0] (which represents 0915)
```

This code includes:
1. The neural predicate declarations for result and carry predictions
2. The slot rule that combines both neural network predictions
3. The recursive add_numbers predicate that processes digit pairs with carry
4. Base cases for empty lists with optional final carry
5. The example would compute 347 + 568 = 0915 (represented as [5,1,9,0] in reverse digit order)

The code follows the described bit-by-bit addition process while maintaining the Problog syntax and avoiding the '->' symbol as requested.