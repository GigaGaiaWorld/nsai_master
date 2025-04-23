nn(mnist_net1, [X], Y, [0,1]) :: event1(X, Y).
nn(mnist_net2, [X], Y, [2,3]) :: event2(X, Y).

% Define coin1 and coin2 to extract event information
coin1(ID1, T) :-
    happensAt(X, Y, T), 
    event1(X, ID1).

coin2(ID2, T) :-
    happensAt(X, Y, T), 
    event2(Y, ID2).

% Define the event table mapping event combinations to event IDs
event_table(ID1, ID2, 0) :- ID1 = 0, ID2 = 2.
event_table(ID1, ID2, 1) :- ID1 = 0, ID2 = 3.
event_table(ID1, ID2, 2) :- ID1 = 1, ID2 = 2.
event_table(ID1, ID2, 3) :- ID1 = 1, ID2 = 3.

% Define detectEvent to detect events at specific timestamps
detectEvent(EventID, T) :-
    coin1(ID1, T),
    coin2(ID2, T),
    event_table(ID1, ID2, EventID).


%================%================%================%================%
% 如果 detectEvent 得到的 EventID 为0或3，则 win=1
result(win=1, T) :-
    detectEvent(EventID, T),
    (EventID = 0 ; EventID = 3).

% 如果 detectEvent 得到的 EventID 为1或2，则 win=0
result(win=0, T) :-
    detectEvent(EventID, T),
    (EventID = 1 ; EventID = 2).
%================%================%================%================%