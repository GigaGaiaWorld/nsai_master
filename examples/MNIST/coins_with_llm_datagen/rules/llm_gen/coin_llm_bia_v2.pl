nn(mnist_net1,[X],Y,[0,1]) :: event1(X,Y).
nn(mnist_net2,[X],Y,[2,3]) :: event2(X,Y).

% Coin predicates for event1 and event2
coin1(ID1, T) :-
    happensAt(X,_,T), 
    event1(X, ID1).

coin2(ID2, T) :-
    happensAt(_,Y,T), 
    event2(Y, ID2).

% Rule for game output based on difference between event1 and event2
result(win=1, T) :-
    coin1(ID1, T),
    coin2(ID2, T),
    abs(ID1 - ID2) =:= 2.

result(win=0, T) :-
    coin1(ID1, T),
    coin2(ID2, T),
    abs(ID1 - ID2) =\= 2.

% Additional rule 1: Timestamp between 50 and 250, event1=1, event2=3
result(win=0, T) :-
    T >= 50,
    T =< 250,
    coin1(1, T),
    coin2(3, T).

% Additional rule 2: Timestamp between 100 and 300, event1=0, event2=3
result(win=1, T) :-
    T >= 100,
    T =< 300,
    coin1(0, T),
    coin2(3, T).