nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).
t(0.1) :: noisy.
1/19::uniform(X,Y,0);1/19::uniform(X,Y,1);1/19::uniform(X,Y,2);1/19::uniform(X,Y,3);1/19::uniform(X,Y,4);1/19::uniform(X,Y,5);1/19::uniform(X,Y,6);1/19::uniform(X,Y,7);1/19::uniform(X,Y,8);1/19::uniform(X,Y,9);1/19::uniform(X,Y,10);1/19::uniform(X,Y,11);1/19::uniform(X,Y,12);1/19::uniform(X,Y,13);1/19::uniform(X,Y,14);1/19::uniform(X,Y,15);1/19::uniform(X,Y,16);1/19::uniform(X,Y,17);1/19::uniform(X,Y,18).
addition_noisy(X,Y,Z) :- digit(X,A), digit(Y,B), (noisy, uniform(_,_,C), Z is (A+B+C) mod 19; Z is (A+B) mod 19.