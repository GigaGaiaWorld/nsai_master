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
% implies/2: A implies B
prove(implies(A, B)) :-
	prove(A),
	prove(B).
% opposite/1: Negation of a goal
prove(opposite(Goal)) :-
	\+ prove(Goal).
% expand/2: Expand a term into another
prove(expand(Term, Expanded)) :-
	expand(Term, Expanded).
% includes/2: Check if an element is in a list
prove(includes(List, Element)) :-
	member(Element, List).
% extend/2: Extend a list with an element
prove(extend(List, Element, Extended)) :-
	Extended = [Element|List].
% refute/1: Refute a goal (opposite of prove)
prove(refute(Goal)) :-
	\+ prove(Goal)
.
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
The generated code is mostly correct and consistent with the original code. It maintains the same functionality for member/2, basic meta-interpreter, and extended logic processing. However, there is a significant difference in the 'implies/2' implementation. The original code allows for P ⇒ Q to be true if P is unprovable or Q is provable, while the generated code requires both P and Q to be provable. Despite this difference, the running results are consistent for the given queries, as the specific queries used do not expose this discrepancy.