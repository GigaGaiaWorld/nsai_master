:- use_module(library(lists), [ member/2, append/2 as list_concat]).
% :- use_module('examples/MNIST/model/addition.py').

nn(mnist_net1,[X],Y,[0,1]) :: event1(X,Y). % ev1 0,1
nn(mnist_net2,[X],Y,[2,3]) :: event2(X,Y). % ev2 2,3
%===%============================================================%===%
%============given window size and number of identicals:=============%
givenRemaining(4).      % corresponding to: remaining
requiredOccurrences(3). % corresponding to: num_of_ident
%===%============================================================%===%
%======================define of simple events:======================%


%===%=============================2==============================%===%
%=====================consider more timestamps:======================%
% In the window of size Remaining, if ??? (not necessarily consecutive) events occur,
% then detectEvent(sequence = EventID, T) is true with event EventID and timestamp T.
detectEvent(sequence = EventID, T) :-
    givenRemaining(Remaining),
    requiredOccurrences(N),
    occursNTimes(EventID, N, Remaining, T).

% if requiredOccurrences reduce to 0, then correct
occursNTimes(_, 0, Remaining, _):- Remaining >= 0.

occursNTimes(EventID, N, Remaining, T) :-
    Remaining > 0,
    N > 0,
    T >= 0,
    happensAt(Y, T),
    event(Y, EventID),
    N1 is N - 1,
    NextRemaining is Remaining - 1,
    allTimeStamps(Timestamps),
    previousTimeStamp(T, Timestamps, Tprev),
    occursNTimes(EventID, N1, NextRemaining, Tprev).

occursNTimes(EventID, N, Remaining, T) :-
    Remaining > 0,
    T >= 0,
    happensAt(Y, T),
    event(Y, EventID2),  
    EventID2 \= EventID,
    NextRemaining is Remaining - 1,
    allTimeStamps(Timestamps),
    previousTimeStamp(T, Timestamps, Tprev),
    occursNTimes(EventID, N, NextRemaining, Tprev).

%===%============================================================%===%
%==================define previous/next timestamps:==================%
previousTimeStamp(T, Timestamps, Tprev):- Tprev is T - 1, Tprev > 0, member(Tprev, Timestamps).
nextTimeStamp(T, Timestamps, Tnext):- T > 0, Tnext is T + 1, member(Tnext, Timestamps).