% The training result is awful, it seem that we have to define event1, event2,... for each network
%[[  2 199]
% [  4 204]]

nn(mnist_net1, [X], Y, [0,1]) :: event(X, Y).
nn(mnist_net2, [M], N, [2,3]) :: event(M, N).

% Define coin1 and coin2 to extract event information
coin(ID, T) :-
    happensAt(X, T), 
    event(X, ID).

% Define the event table mapping event combinations to event IDs
event_table(ID1, ID2, 0) :- ID1 = 0, ID2 = 2.
event_table(ID1, ID2, 1) :- ID1 = 0, ID2 = 3.
event_table(ID1, ID2, 2) :- ID1 = 1, ID2 = 2.
event_table(ID1, ID2, 3) :- ID1 = 1, ID2 = 3.

% Define detectEvent to detect events at specific timestamps
detectEvent(EventID, T) :-
    coin(ID1, T),
    coin(ID2, T),
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