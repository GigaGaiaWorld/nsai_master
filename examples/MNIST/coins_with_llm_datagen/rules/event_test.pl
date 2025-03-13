nn(mnist_net1,[X],Y,[0,1]) :: event1(X,Y).
nn(mnist_net2,[X],Y,[2,3]) :: event2(X,Y).

coin(ID1, T) :-
    happensAt(X,Y,T), 
    event1(X, ID1).
coin(ID2, T) :-
    happensAt(X,Y,T), 
    event2(Y, ID2).