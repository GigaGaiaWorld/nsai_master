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
	
\+ prove(P); prove(Q)
.
prove(opposite(P)) :-
	
\+ prove(P)
.
prove(expand(A,B)) :-
	expand(A,B).
prove(includes(Set,X)) :-
	member(X,Set).
prove(extend(List,Elem,Extended)) :-
	
Extended = [Elem|List]
.
prove(refute(P)) :-
	\+ prove(P).
% --------- Examples ---------- %
% Define some expand rules:
expand(double(X), Y) :- Y is X*2.
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

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is mostly correct and consistent with the original code. It maintains all the essential functionalities, including the basic meta-interpreter and extended logic processing. However, the generated code lacks the 'square' expand rule present in the original code, which could affect queries involving this rule. Despite this omission, the provided queries do not utilize the missing rule, so the results remain consistent.
*/