nn(mnist_net1,[X1],Y1,[0,2]) :: event(X1,Y1).
nn(mnist_net2,[X2],Y2,[1,3]) :: event(X2,Y2).

detectEvent(sequence = ID, T) :- % class: 3
    happensAt(X, T), event(X, ID).

% detectEvent(sequence = 1, T) :- % class: 1
%     happensAt(X, T),
%     event(X, 1).



 