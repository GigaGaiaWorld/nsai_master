% %=================%================= NOT USED AT ALL =================%=================%
% %=================%================= NOT USED AT ALL =================%=================%

% nn(mnist_net,[X],Y,[0,other]) :: event(X,Y).

% %===%============================================================%===%
% %===================consider only two timestamps:====================%
% % thought: identifies sequences where the same digit appears consecutively.
% % initAtDigit(sequence = Y, T) :-
% %     % at the current timestamp
% %     happensAt(X, T),
% %     digit(X, Y),

% %     % at the previous timestamp
% %     happensAt(Xprev, Tprev),
% %     digit(Xprev, Y),

% %     % timestamps
% %     allTimeStamps(Timestamps),
% %     previousTimeStamp(T, Timestamps, Tprev),
% %     Tprev >= 0.


% %===%============================================================%===%
% %=====================consider more timestamps:======================%
% givenRemaining(4).

% % In the window of size Remaining, if two (not necessarily consecutive) events occur,
% % then initAtDigit(sequence = EventID, T) is true with event EventID and timestamp T.
% initAtEvent(sequence = EventID, T) :-                   % 
%     givenRemaining(Remaining),                          % 
%     sequenceEndingAt([EventID, EventID], Remaining, T). % 


% % An empty sequence will always be within
% sequenceWithin([], _, _).

% % Case1: A sequence can be within Remaining of T if it end at T:
% sequenceWithin(L, Remaining, T) :-
%     sequenceEndingAt(L, Remaining, T).

% % Case2: If Remaining>0, check with recursion: sequenceWithin of last timestamp.
% sequenceWithin(L, Remaining, T) :-
%     Remaining > 0,
%     T >= 0,
%     NextRemaining is Remaining - 1,
%     allTimeStamps(Timestamps),
%     previousTimeStamp(T, Timestamps, Tprev),
%     sequenceWithin(L, NextRemaining, Tprev).


% % A sequence will start at T and be within Remaining if X happens at T and the rest of the sequence is within NextRemaining of Tprev
% sequenceEndingAt([X | L], Remaining, T) :-
%     Remaining > 0,
%     T >= 0,
%     happensAt(Y, T),
%     event(Y, X),
%     NextRemaining is Remaining - 1,
%     allTimeStamps(Timestamps),
%     previousTimeStamp(T, Timestamps, Tprev),
%     sequenceWithin(L, NextRemaining, Tprev).

% % we could define more different "initAt" for other scenarios...


% previousTimeStamp(T, Timestamps, Tprev):- Tprev is T - 1.
% nextTimeStamp(T, Timestamps, Tnext):- Tnext is T + 1.

% % sdFluent( aux ).

% %==================all timestamps will be inserted here===================%
% % allTimeStamps([...])

% %==================all happensAt will be inserted here====================%
% % in happensAt(X, T), X indicates the Event ID, T indicates the timestamp of this event.
% % we could understand happensAt(X, T) as the time window, but we don't know it's content.
% % we could understand digit(X, Y) as the content of the time window.
