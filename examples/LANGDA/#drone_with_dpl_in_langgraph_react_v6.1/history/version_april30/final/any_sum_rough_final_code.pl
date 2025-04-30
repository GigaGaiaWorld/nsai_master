nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).
addition(X,Y,Z) :- digit(X,X2), digit(Y,Y2), Z is X2+Y2.
anysum(Bag,R) :- 
bag_sum(Bag, 0, R).\nbag_sum([], Acc, Acc).\nbag_sum([X|Xs], Acc, R) :- digit(X, Val), NewAcc is Acc + Val, bag_sum(Xs, NewAcc, R).