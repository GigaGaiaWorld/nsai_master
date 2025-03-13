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
% 当时间在50到250之间，且 event1 的分类为1、event2 为3时，
% 即(ID1,ID2) = (1,3)，虽然基本规则会映射为 EventID=3（win=1），
% 此时应将win改为0。
result(win=0, T) :-
    happensAt(X, Y, T),
    T >= 50, T =< 250,
    event1(X, 1),
    event2(Y, 3).

% 当时间在100到300之间，且 event1 的分类为0、event2 为3时，
% 即(ID1,ID2) = (0,3)，虽然基本规则会映射为 EventID=1（win=0），
% 此时应将win改为1。
result(win=1, T) :-
    happensAt(X, Y, T),
    T >= 100, T =< 300,
    event1(X, 0),
    event2(Y, 3).

% 如果 detectEvent 得到的 EventID 为0或3，则 win=1
result(win=1, T) :-
    detectEvent(EventID, T),
    (EventID = 0 ; EventID = 3).

% 如果 detectEvent 得到的 EventID 为1或2，则 win=0
result(win=0, T) :-
    detectEvent(EventID, T),
    (EventID = 1 ; EventID = 2).
%================%================%================%================%