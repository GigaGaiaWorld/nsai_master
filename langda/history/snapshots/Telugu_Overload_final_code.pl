% Neural network definitions for different languages
nn(arabic_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: arabic_digit(X,Y).
nn(telugu_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: telugu_digit(X,Y).
nn(urdu_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: urdu_digit(X,Y).
% Convert digit list to number
number([],Result,Result).
number([H|T],Acc,Result) :- 
 
telugu_digit(H,Nr)
, 
 Acc2 is Nr+10*Acc, number(T,Acc2,Result).
number(X,Y) :- number(X,0,Y).
% Anomaly detection logic - Result is 1 if anomaly detected, 0 otherwise
anomaly_detection(Digit1, Digit2, 1) :- 
 
number(Digit1, Current1), number(Digit2, Current2), Sum is Current1 + Current2, Sum > 150
.
anomaly_detection(Digit1, Digit2, 0) :- \+ anomaly_detection(Digit1, Digit2, 1).
/* %%% Result %%% 
% Problog Inference Result：

*/