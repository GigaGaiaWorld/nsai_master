nn(mnist_net1,[X],Y,[0,1]) :: event1(X,Y).
nn(mnist_net2,[X],Y,[2,3]) :: event2(X,Y).

% Coin predicates for event1 and event2
coin1(ID1, T) :-
    happensAt(X,Y, T), 
    event1(X, ID1).

coin2(ID2, T) :-
    happensAt(X,Y, T), 
    event2(Y, ID2).

% Event table mapping
event_table(ID1,ID2,0) :- ID1=0, ID2=2.
event_table(ID1,ID2,1) :- ID1=0, ID2=3.
event_table(ID1,ID2,2) :- ID1=1, ID2=2.
event_table(ID1,ID2,3) :- ID1=1, ID2=3.

% Detect event based on table
detectEvent(EventID, T) :-
    coin1(ID1, T),
    coin2(ID2, T),
    event_table(ID1,ID2,EventID).

result(win=1, T) :-
    % Get the detected event ID at time T
    detectEvent(EventID, T),
    % Retrieve the corresponding event1 and event2 labels from the event table
    event_table(ID1, ID2, EventID),
    % Check if the absolute difference between the labels is 2
    abs(ID1 - ID2) =:= 2.

result(win=0, T) :-
    % Get the detected event ID at time T
    detectEvent(EventID, T),
    % Retrieve the corresponding event1 and event2 labels from the event table
    event_table(ID1, ID2, EventID),
    % Check if the absolute difference between the labels is not 2
    abs(ID1 - ID2) =\= 2.