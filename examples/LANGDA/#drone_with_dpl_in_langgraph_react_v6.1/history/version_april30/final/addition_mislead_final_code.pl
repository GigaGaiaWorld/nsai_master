
nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9])
 :: digit(X,Y).
number([],Result,Result).
number([H|T],Acc,Result) :- 
digit(H,D), NewAcc is Acc + (D * (10 ^ length(T))), number(T, NewAcc, Result)
number(X,Y) :- number(X,0,Y).
multi_addition(X,Y,Z) :- 
number(X, 0, X1), number(Y, 0, Y1), Z is X1 + Y1
addition(X,Y,Z) :- 
digit(X1, D1), digit(X2, D2), Z is D1 + D2