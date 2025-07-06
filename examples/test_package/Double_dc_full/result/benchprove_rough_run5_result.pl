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
prove(implies(A, B)) :- prove(A), prove(B).
prove(opposite(Goal)) :- \+ prove(Goal).
prove(expand(Goal, Result)) :- expand(Goal, Result).
prove(includes(List, Elem)) :- member(Elem, List).
prove(extend(List, Elem, [Elem|List])).
prove(refute(Goal)) :- \+ prove(Goal).
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

/* Result Report:
Validity_form: False
Validity_result: True
Report: The generated code is mostly correct and consistent with the original code in terms of functionality. However, there is a significant difference in the implementation of the 'implies' predicate. The original code correctly implements P ⇒ Q as 'P is unprovable or Q is provable', while the generated code incorrectly implements it as 'prove A and prove B', which is equivalent to A ∧ B. This is a logical error. Despite this, the running results are consistent for the given queries because the specific test cases happen to work with both implementations in this context.
*/