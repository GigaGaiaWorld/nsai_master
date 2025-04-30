nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).
addition(X,Y,Z) :- digit(X,X2), digit(Y,Y2), Z is X2+Y2.
anysum(Bag,R) :- 
anysum([], 0).\nanysum([H|T], R) :- digit(H, D), anysum(T, R1), R is R1 + D.