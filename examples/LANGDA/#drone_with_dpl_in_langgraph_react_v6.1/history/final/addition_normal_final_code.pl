
nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9])
 :: digit(X,Y).
number([],Result,Result).
number([H|T],Acc,Result) :- 
digit(H,D), NewAcc is Acc + (D * (10 ^ length(T))), number(T, NewAcc, Result)
number(X,Y) :- number(X,0,Y).
multi_addition(X,Y,Z) :- 
number(X, 0, XVal), number(Y, 0, YVal), Z is XVal + YVal
addition(X,Y,Z) :- 
digit(X,XVal), digit(Y,YVal), Z is XVal + YVal