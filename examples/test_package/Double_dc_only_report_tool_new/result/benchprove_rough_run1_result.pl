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
prove(implies(A, B)) :- \+ prove(A).
prove(implies(A, B)) :- prove(A), prove(B).
prove(opposite(A)) :- \+ prove(A).
prove(expand(Term, Result)) :- expand(Term, Result).
prove(includes(List, Elem)) :- member(Elem, List).
prove(extend(List, Elem, [Elem | List])).
prove(refute(A)) :- \+ prove(A).
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
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in terms of functionality and logic. It properly implements the meta-interpreter and extended logic processing, including the handling of implies, opposite, expand, includes, extend, and refute. The generated code simplifies the implies/2 predicate into two separate clauses, which is logically equivalent to the original. All other predicates remain unchanged. The running results of both codes are identical, confirming the correctness of the generated code.
*/