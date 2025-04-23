lann(mnist_net:"mnist network",[X],Y,[0,1,2,3,4,5,6,7,8,9]:"pick the output from one of there value") :: digit(X,Y).


number([],Result,Result).
number([H|T],Acc,Result) :- langda(NET:"use mnist network",LLM:"Recursively process the image list: identify the digits one by one and construct the corresponding multi-bit integers in low-bit first order.").
number(X,Y) :- number(X,0,Y).

multi_addition(X,Y,Z) :- langda(NET:"use mnist network",LLM:"Convert two sets of sequences consisting of digital pictures into integers and add them together to get the numerical result.").
addition(X,Y,Z) :- langda(NET:"use mnist network",LLM:"Use a neural network to identify the numbers in two pictures and then calculate their sum. Try to use X1 and X2 as term first").
