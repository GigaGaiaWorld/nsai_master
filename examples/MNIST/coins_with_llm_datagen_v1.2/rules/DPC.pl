nn(mnist_net2, [X], Y, [2,3]) :: wrapper(X, Y).
% <<DeepProbCEP: A neuro-symbolic approach for complex event processing in adversarial settings>>
% Main interface for the framework. 
sequence(L, W, T) : 
    % Reverse list to simplify rule definitions 
    reverse(L, L2), 
    sequenceEndingAt(L2, W, T).  

sequenceEndingAt([X | L], W, T) :
    W > 0, T >= 0, 
    happensAt(Y, T), 
    wrapper(Y, X), 
    NextW is W - 1, 
    allTimeStamps(Timestamps), 
    previousTimeStamp(T, Timestamps, Tprev), 
    sequenceWithin(L, [], NextW, Tprev). 

% An empty sequence will be within if Excluded % elements is empty or if W is 0 
sequenceWithin([], [], _, _). sequenceWithin([], _, 0, _). 

% If we have detected all simple events but still % have Excluded elements, check until the end of the window 
sequenceWithin([], E, W, T) :
    W > 0, 
    happensAt(H, T), 
    wrapper(H, Y), 
    \+ itemIn(Y, E), 
    NextW is W - 1, 
    allTimeStamps(Timestamps), 
    previousTimeStamp(T, Timestamps, Tprev), 
    sequenceWithin([], E, NextW, Tprev). 

% A sequence can be within T if it ends at T 
sequenceWithin(L, E, W, T) :- 
    sequenceEndingAt(L, W, T). 

% If the next element in the list is a negation, add it to E 
sequenceWithin([X | L], E, W, T) :
    isNegation(X, Y), 
    sequenceWithin(L, [Y | E], W, T). 

% A sequence can be within W of T if it is within NextW of Tprev 
sequenceWithin([X | L], E, W, T) :
    W > 0, 
    T >= 0, 
    \+ isNegation(X, _), 
    happensAt(H, T), 
    wrapper(H, Y), 
    \+ itemIn(Y, E), 
    NextW is W - 1, 
    allTimeStamps(Timestamps), 
    previousTimeStamp(T, Timestamps, Tprev), 
    sequenceWithin([X | L], E, NextW, Tprev).