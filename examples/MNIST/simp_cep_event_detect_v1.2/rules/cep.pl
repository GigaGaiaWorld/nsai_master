nn(mnist_net1,[X1],Y1,[0,1]) :: event1(X1,Y1).
nn(mnist_net2,[X2],Y2,[2,3]) :: event2(X2,Y2).

outcome1(ID, T) :- % class: 
    happensAt(X, T), event1(X, ID).
outcome1(none, T) :- % class: 
    happensAt(X, T), \+event1(X, _).

outcome2(ID, T) :- % class: 
    happensAt(X, T), event2(X, ID).
outcome2(none, T) :- % class: 
    happensAt(X, T), \+event2(X, _).

detectEvent(sequence = ID, T) :- 
    (outcome1(ID, T),outcome2(none, T));
    (outcome1(none, T),outcome2(ID, T)).