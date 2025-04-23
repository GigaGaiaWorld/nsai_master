:- use_module(library(lists), [ member/2, append/2 as list_concat]).
% :- use_module('examples/MNIST/model/addition.py').

nn(mnist_net1,[X],Y,[0,1]) :: event(X,Y). % ev1 0,1
nn(mnist_net2,[X],Y,[2,3]) :: event(X,Y). % ev2 2,3
%===%============================================================%===%
%============given window size and number of identicals:=============%
givenRemaining(3).      % corresponding to: remaining
requiredOccurrences(2). % corresponding to: num_of_ident


%===%=============================2==============================%===%
%=====================consider more timestamps:======================%

detectEvent(sequence = EventID, T) :-
    givenRemaining(Remaining),
    requiredOccurrences(N),
    countOccurrences(EventID, Remaining, T, Count),
    Count >= N.

detectEvent(sequence = none, T) :-
    \+ (givenRemaining(Remaining),
        requiredOccurrences(N),
        countOccurrences(_, Remaining, T, Count),
        Count >= N).

% Base case: when Remaining is 0 or T is invalid
countOccurrences(_, 0, _, 0).
countOccurrences(_, _, T, 0) :- T < 0.

% Count occurrences of EventID within the window
countOccurrences(EventID, Remaining, T, Count) :-
    Remaining > 0,
    T >= 0,
    happensAt(Y, T),
    allTimeStamps(Timestamps),
    previousTimeStamp(T, Timestamps, Tprev),
    NextRemaining is Remaining - 1,
    (
        % If current event matches EventID, add 1 to count
        (event(Y, EventID), 
         countOccurrences(EventID, NextRemaining, Tprev, PrevCount),
         Count is PrevCount + 1)
        ;
        % If current event doesn't match EventID, continue without adding
        (event(Y, OtherID), OtherID \= EventID,
         countOccurrences(EventID, NextRemaining, Tprev, Count))
    ).

%===%============================================================%===%
%==================define previous/next timestamps:==================%
previousTimeStamp(T, Timestamps, Tprev):- Tprev is T - 1, Tprev > 0, member(Tprev, Timestamps).
nextTimeStamp(T, Timestamps, Tnext):- T > 0, Tnext is T + 1, member(Tnext, Timestamps).