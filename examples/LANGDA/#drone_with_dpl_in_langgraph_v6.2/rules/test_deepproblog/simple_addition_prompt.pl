lann(mnist_net:"mnist network",[X],Y,[0,1,2,3,4,5,6,7,8,9]:"pick the output from one of these values") :: digit(X,Y).


langda(LLM:"",FUP:"False").
addition(X,Y,Z) :- langda(NET:"use mnist network",LLM:"Use a neural network to identify the numbers in two pictures and then calculate their sum.").

