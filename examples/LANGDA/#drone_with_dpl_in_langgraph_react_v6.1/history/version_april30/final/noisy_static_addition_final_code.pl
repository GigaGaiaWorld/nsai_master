nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).
t(0.1) :: noisy.
uniform(X,Y,V) :- between(0,18,V), V is floor((random * 19)).
addition_noisy(X,Y,Z) :- noisy, uniform(X,Y,Z).
addition_noisy(X,Y,Z) :- \+noisy, digit(X,N1), digit(Y,N2), Z is N1+N2.
addition(X,Y,Z) :- digit(X,N1), digit(Y,N2), Z is N1+N2.