nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).
number([],Result,Result).
number([H|T],Acc,Result) :- digit(H,Nr), Acc2 is Nr+10*Acc,number(T,Acc2,Result).
number(X,Y) :- number(X,0,Y).
anomaly_detection(Digit1, Digit2, Result) :- 
 
 
    number(Digit1, X),
    number(Digit2, Y),
    (X =:= Y, Result = 1 ; X =\= Y, Result = 0).
/* %%% Result %%% 
% Problog Inference Result：

*/