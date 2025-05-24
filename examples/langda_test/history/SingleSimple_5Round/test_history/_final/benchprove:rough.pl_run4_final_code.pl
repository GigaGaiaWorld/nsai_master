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
prove(true).
prove(Goal) :-
	clause(Goal, Body),
	prove(Body).
prove((A,B)) :-
	prove(A),
	prove(B).
prove(implies(A,B)) :-
	prove(A),
	prove(B).
prove(opposite(A)) :-
	not(prove(A)).
prove(expand(Goal, Result)) :-
	expand(Goal, Result).
prove(includes(List, Elem)) :-
	member(Elem, List).
prove(extend(List, Elem, NewList)) :-
	NewList = [Elem|List].
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
Validity_form:False\Validity_result:True
The generated code is mostly correct and consistent with the original code in terms of functionality and results. However, there are some redundancies in the generated code, such as the duplicate definitions of 'prove(true)' and 'prove(Goal)'. The 'implies' predicate in the generated code is incorrectly defined as requiring both A and B to be provable, which differs from the original's definition (P is unprovable or Q is provable). Despite this, the running results are consistent with the original code for the given queries.