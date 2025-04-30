
nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9])
 :: digit(X,Y).
digit(X,Y) :- nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]).
addition(X,Y,Z) :- 
digit(X,A), digit(Y,B), Z is A+B.