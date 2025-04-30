nn(rnn,[Text],Embedding) :: rnn(Text,Embedding).
nn(nn_permute, [X],Y,[0,1,2,3,4,5]) :: net1(X,Y).
nn(nn_op1, [X],Y, [plus,minus,times,div]) :: net2(X,Y).
nn(nn_swap, [X],Y, [no_swap,swap]) :: net3(X,Y).
nn(nn_op2, [X],Y, [plus,minus,times,div]) :: net4(X,Y).
permute(0,A,B,C,A,B,C).
permute(1,A,B,C,A,C,B).
permute(2,A,B,C,B,A,C).
permute(3,A,B,C,B,C,A).
permute(4,A,B,C,C,A,B).
permute(5,A,B,C,C,B,A).
swap(no_swap,X,Y,X,Y).
swap(swap,X,Y,Y,X).
operator(plus,X,Y,Z) :- Z is X+Y.
operator(minus,X,Y,Z) :- Z is X-Y.
operator(times,X,Y,Z) :- Z is X*Y.
operator(div,X,Y,Z) :- Y > 0, 0 =:= X mod Y,Z is X//Y.
wap(Text,X1,X2,X3,Out) :-
rnn(Text,Embedding),
net1(Embedding,P),
permute(P,X1,X2,X3,A,B,C),
net3(Embedding,SwapDecision),
swap(SwapDecision,B,C,B1,C1),
min(A,B1,Min1),
max(A,B1,Max1),
min(Min1,C1,Min2),
max(Max1,C1,Max2),
net2(Embedding,Op1),
operator(Op1,Min1,Min2,Sum),
net4(Embedding,Op2),
operator(Op2,Sum,Max2,Out).

min(X,Y,X) :- X =< Y.
min(X,Y,Y) :- Y < X.
max(X,Y,X) :- X >= Y.
max(X,Y,Y) :- Y > X.