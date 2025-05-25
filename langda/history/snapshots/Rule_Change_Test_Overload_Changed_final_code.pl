nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).
% Please use number/2 to transform digit to real numbers
number([],Result,Result).
number([H|T],Acc,Result) :- digit(H,Nr), Acc2 is Nr+10*Acc,number(T,Acc2,Result).
number(X,Y) :- number(X,0,Y).
% If the sum of the currents of the two branches exceeds the specified value, it indicates an abnormality. If there's anomaly, Result is 1, otherwise, Result is 0.
% Case 1: Ambient temperature ≤ 30 °C, the total current-carrying capacity is about 150 A.
% Case 2: Ambient temperature ≥ 50 °C, the total current-carrying capacity is reduced to about 100 A.
anomaly_detection(Digit1, Digit2, Result) :- 
 
 number(Digit1, Num1), number(Digit2, Num2), TotalCurrent is Num1 + Num2, (TotalCurrent > 100, Result = 1 ; TotalCurrent =< 100, Result = 0).
/* %%% Result %%% 
% Problog Inference Result：

*/