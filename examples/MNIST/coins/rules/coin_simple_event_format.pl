nn(mnist_net1,[X],Y,[0,1]) :: event1(X,Y).
nn(mnist_net2,[X],Y,[2,3]) :: event2(X,Y).

% 保持原始的coin1和coin2定义不变
coin1(ID1, T) :-
    happensAt(X,Y,T), 
    event1(X, ID1).
coin2(ID2, T) :-
    happensAt(X,Y,T), 
    event2(Y, ID2).

% ====== according to the "possible" event combinations, the event table should be generated automatically!
event_table(ID1,ID2,0) :- ID1=0, ID2=2.
event_table(ID1,ID2,1) :- ID1=0, ID2=3.
event_table(ID1,ID2,2) :- ID1=1, ID2=2.
event_table(ID1,ID2,3) :- ID1=1, ID2=3.

% ===== this is only for combining events together, nothing more
detectEvent(EventID, T) :-
    coin1(ID1, T),
    coin2(ID2, T),
    event_table(ID1,ID2,EventID).

% ===== some complex rules about is it "win" or not.
% game(...) :- ...