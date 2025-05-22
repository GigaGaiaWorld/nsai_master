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
prove(opposite(Goal)) :- 
	not(prove(Goal)).
prove(expand(Term, Result)) :- 
	expand(Term, Result).
prove(includes(List, Elem)) :- 
	member(Elem, List).
prove(extend(List, Elem, Result)) :- 
	Result = [Elem|List].
prove(refute(Goal)) :- 
	not(prove(Goal)).
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
The generated code is mostly correct and consistent with the original code in terms of functionality. However, there are some redundancies, such as the duplicate definitions of 'prove(true)', 'prove(Goal)', and 'prove((A,B))'. The logic for 'prove(implies(A,B))' in the generated code is incorrect as it requires both A and B to be provable, whereas the original code correctly implements the implication (A ⇒ B) by checking if A is unprovable or B is provable. Despite this, the running results are consistent with the original code for the given queries.