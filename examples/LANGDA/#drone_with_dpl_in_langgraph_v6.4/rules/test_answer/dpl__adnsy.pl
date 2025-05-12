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

0.1 :: noisy.

1/19::uniform(X,Y,0);1/19::uniform(X,Y,1);1/19::uniform(X,Y,2);1/19::uniform(X,Y,3);1/19::uniform(X,Y,4);1/19::uniform(X,Y,5);1/19::uniform(X,Y,6);1/19::uniform(X,Y,7);1/19::uniform(X,Y,8);1/19::uniform(X,Y,9);1/19::uniform(X,Y,10);1/19::uniform(X,Y,11);1/19::uniform(X,Y,12);1/19::uniform(X,Y,13);1/19::uniform(X,Y,14);1/19::uniform(X,Y,15);1/19::uniform(X,Y,16);1/19::uniform(X,Y,17);1/19::uniform(X,Y,18).

addition_noisy(X,Y,Z) :- noisy, uniform(X,Y,Z).
addition_noisy(X,Y,Z) :- \+noisy, digit(X,N1), digit(Y,N2), Z is N1+N2.

addition(X,Y,Z) :- digit(X,N1), digit(Y,N2), Z is N1+N2. 

query(addition_noisy(img_5,img_6,Z)).