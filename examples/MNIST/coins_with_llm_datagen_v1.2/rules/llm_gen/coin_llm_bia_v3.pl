nn(mnist_net1,[X],Y,[0,1]) :: event1(X,Y).
nn(mnist_net2,[X],Y,[2,3]) :: event2(X,Y).

coin1(ID1, T) :-
    happensAt(X,Y,T), 
    event1(X, ID1).
coin2(ID2, T) :-
    happensAt(X,Y,T), 
    event2(Y, ID2).

% in the origin code, it doesn't have "T" term
outcome(0, ID1, ID2, T) :-
    T >= 50,
    T =< 250,
    ID1 = 1,
    ID2 = 3.
outcome(1, ID1, ID2, T) :-
    T >= 100,
    T =< 300,
    ID1 = 0,
    ID2 = 3.

outcome(1, ID1, ID2, T) :- (abs(ID1 - ID2) =:= 2).
outcome(0, ID1, ID2, T) :- (abs(ID1 - ID2) =\= 2).

result(win=EventID,T) :-
    coin1(ID1, T),
    coin2(ID2, T),
    outcome(EventID, ID1, ID2, T).