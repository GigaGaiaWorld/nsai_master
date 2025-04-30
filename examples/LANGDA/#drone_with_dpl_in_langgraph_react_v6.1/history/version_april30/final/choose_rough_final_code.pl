nn(neural1,[I1,I2,Carry],O,[0,1,2,3,4,5,6,7,8,9]) :: result(I1,I2,Carry,O).
nn(neural2,[I1,I2,Carry],NewCarry,[0,1]) :: carry(I1,I2,Carry,NewCarry).
%nn(neural1,[I],O,[0,1,2,3,4,5,6,7,8,9]) :: result(I,O).
%nn(neural2,[I],NewCarry,[0,1]) :: carry(I,NewCarry).
slot(I1,I2,Carry,Carry2,O) :-
result(I1,I2,Carry,O),
carry(I1,I2,Carry,Carry2).
%    one_hot(I1,10,T1),
%    one_hot(I2,10,T2),
%    one_hot(Carry,2,T3),
%    cat([T1,T2,T3],T),
%    result(T,O),
%    carry(T,Carry2).
add_bits(I1, I2, Carry, Sum, NewCarry) :-\n    result(I1, I2, Carry, Sum),\n    carry(I1, I2, Carry, NewCarry).\n\nadd_numbers([], [], Carry, [], Carry).\nadd_numbers([I1|T1], [I2|T2], Carry, [Sum|TSum], FinalCarry) :-\n    add_bits(I1, I2, Carry, Sum, NewCarry),\n    add_numbers(T1, T2, NewCarry, TSum, FinalCarry).