nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).

langda(NET:"use mnist network", LLM:"generate the number part that allow us to ")
multi_addition(X,Y,Z) :- number(X,X2),number(Y,Y2), Z is X2+Y2.
addition(X,Y,Z) :- digit(X,X2), digit(Y,Y2), Z is X2+Y2.

