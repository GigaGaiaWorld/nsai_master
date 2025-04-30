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
rnn(Text,Embedding),\nnet1(Embedding,P),\npermute(P,X1,X2,X3,A,B,C),\nnet3(Embedding,SwapDecision),\nswap(SwapDecision,B,C,B1,C1),\nnet2(Embedding,Op1),\noperator(Op1,A,B1,Res1),\nnet4(Embedding,Op2),\noperator(Op2,Res1,C1,Out).