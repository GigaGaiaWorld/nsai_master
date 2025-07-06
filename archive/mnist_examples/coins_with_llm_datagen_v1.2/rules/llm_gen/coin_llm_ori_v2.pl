nn(mnist_net1,[X],Y,[0,1]) :: event1(X,Y).
nn(mnist_net2,[X],Y,[2,3]) :: event2(X,Y).

% Coin predicates for event1 and event2
coin1(ID1, T) :-
    happensAt(X,Y, T), 
    event1(X, ID1).

coin2(ID2, T) :-
    happensAt(X,Y, T), 
    event2(Y, ID2).

result(win=1, T) :-
    % Get the output IDs from both events at time T
    coin1(ID1, T),
    coin2(ID2, T),
    % Calculate the absolute difference between the two outputs
    abs(ID1 - ID2) =:= 2.

result(win=0, T) :-
    % Get the output IDs from both events at time T
    coin1(ID1, T),
    coin2(ID2, T),
    % Check if the absolute difference is not equal to 2
    \+ abs(ID1 - ID2) =:= 2.