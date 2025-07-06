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
prove(implies(Goal1, Goal2)) :- prove(Goal1) -> prove(Goal2).
prove(opposite(Goal)) :- \+ prove(Goal).
prove(expand(Term, Result)) :- expand(Term, Result).
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
Validity_result: False
Report: The generated code attempts to replicate the functionality of the original code but introduces a syntax error in the 'implies' predicate by using '->' incorrectly, which is not valid in this context. The original code correctly uses a disjunction (;) to handle the implication logic. This error makes the generated code invalid and causes it to fail during execution. The rest of the predicates are correctly replicated and should function as intended if not for this error.
*/