% member/2 for ProbLog
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).
% --------- Basic meta-interpreter ---------
% Prove "true" always succeeds
prove(true).
prove(Goal) :-
	% For all other goals, use the clause/2 facts/rules defined in the program
	clause(Goal, Body),
	prove(Body).
% Prove compound goal A,B: prove A first, then prove B
prove((A,B)) :-
	prove(A),
	prove(B).
% --------- Extended logic processing ---------
prove(implies(P,Q)) :-
	
 \+ prove(P); prove(Q).
prove(opposite(P)) :-
	
 \+ prove(P).
prove(expand(A,B)) :-
	
 expand(A, B).
prove(includes(Set,X)) :-
	
 member(X, Set).
prove(extend(List,Elem,Extended)) :-
	
 Extended = [Elem|List].
% 6. refute(P): refute, equivalent to "unprovable"
prove(refute(P)) :-
	\+ prove(P).
% --------- Examples ---------- %
% Define some expand rules:
expand(double(X), Y) :- Y is X*2.
expand(square(X), Y) :- Y is X*X.
parent(alice, bob).
parent(bob, carol).
ancestor(X,Y) :- parent(X,Y).
ancestor(X,Y) :- parent(X,Z), ancestor(Z,Y).
% --------- Queries ---------- %
query(prove(implies(parent(alice,bob), ancestor(alice,bob)))).
query(prove(opposite(parent(carol,alice)))).
query(prove(expand(double(3),6))).
query(prove(includes([a,b,c],b))).
query(prove(extend([1,2],3,[3,1,2]))).

*** Result:*** 
% Problog Inference Result：
prove(implies(parent(alice,bob),ancestor(alice,bob))) = 1.0000
prove(opposite(parent(carol,alice))) = 1.0000
prove(expand(double(3),6)) = 1.0000
prove(includes([a, b, c],b)) = 1.0000
prove(extend([1, 2],3,[3, 1, 2])) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality and logic. The only differences are minor formatting changes, such as spacing and line breaks, which do not affect the code's execution or results. The generated code maintains all the essential components of the original, including the meta-interpreter, extended logic processing, examples, and queries. The running results of both pieces of code are identical, confirming that the generated code meets the expectations.