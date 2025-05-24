nn(arabic_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: arabic_digit(X,Y).
operation(X,Y,Z) :- 
 
 
    arabic_digit(X, DigitX),
    arabic_digit(Y, DigitY),
    Z is DigitX + DigitY.

%%% Result %%% 
% Problog Inference Result：
