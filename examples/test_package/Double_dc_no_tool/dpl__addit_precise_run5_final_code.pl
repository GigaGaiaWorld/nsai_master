digit(img_1,1).
digit(img_2,2).
digit(img_3,3).
digit(img_4,4).
digit(img_5,5).
digit(img_6,6).
digit(img_7,7).
digit(img_8,8).
digit(img_9,9).
digit(img_0,0).
number([],Result,Result).
number([Img|Imgs], Acc, Result) :- digit(Img, Nr), NewAcc is Acc * 10 + Nr, number(Imgs, NewAcc, Result).
number(X,Y) :- number(X,0,Y).
multi_addition(X,Y,Z) :- 
 number(X, XNum), number(Y, YNum), Z is XNum + YNum.
query(multi_addition([img_7,img_9],[img_3,img_1,img_2],Z)).
/* %%% Result %%% 
% Problog Inference Result：
multi_addition([img_7, img_9],[img_3, img_1, img_2],391) = 1.0000
*/