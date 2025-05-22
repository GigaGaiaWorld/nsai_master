nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).

t(0.1) :: noisy.

langda(LLM:"For any X and Y, the value V of the predicate uniform(X,Y,V) is chosen randomly from the integers 0 to 18 with equal probability (1/19).").

addition_noisy(X,Y,Z) :- noisy, uniform(X,Y,Z).
addition_noisy(X,Y,Z) :- \+noisy, digit(X,N1), digit(Y,N2), Z is N1+N2.

addition(X,Y,Z) :- digit(X,N1), digit(Y,N2), Z is N1+N2. 