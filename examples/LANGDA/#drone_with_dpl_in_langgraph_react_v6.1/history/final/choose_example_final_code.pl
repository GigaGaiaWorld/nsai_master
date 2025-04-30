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
add_numbers([],[],C,[C]) :- C > 0.
add_numbers([],[],_,[]).
add_numbers([H1|T1],[H2|T2],C0,[O|T]) :-
    slot(H1,H2,C0,C1,O),
    add_numbers(T1,T2,C1,T).