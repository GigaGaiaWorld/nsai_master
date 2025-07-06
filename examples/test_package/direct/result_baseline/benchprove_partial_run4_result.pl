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
	langda(LLM:"P is unprovable or Q is provable").

prove(opposite(P)) :-
	langda(LLM:"P is unprovable").

prove(expand(A,B)) :-
	expand(A,B).

prove(includes(Set,X)) :-
	member(X,Set).

prove(extend(List,Elem,Extended)) :-
	langda(LLM:"add Elem to the head of List to get Extended").

prove(refute(P)) :-
	\+ prove(P).

% --------- Examples ---------- %
% Define some expand rules:
langda(LLM:"define expand/2: Y is X*2").

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

% Predicted results by DeepSeek:
% result1: prove(implies(parent(alice,bob), ancestor(alice,bob))) :- true.
result2: prove(opposite(parent(carol,alice))) :- true.
result3: prove(expand(double(3),6)) :- true.
result4: prove(includes([a,b,c],b)) :- true.
result5: prove(extend([1,2],3,[3,1,2])) :- true.

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is mostly correct and consistent with the original code. It includes definitions for the required predicates (implies, opposite, expand, includes, extend) and correctly implements the meta-interpreter for proving goals. The generated code also includes the necessary examples and queries to match the original results. However, the 'langda' predicate usage is unconventional and might not be standard Prolog/ProbLog syntax, which could cause issues in some implementations. The results predicted by DeepSeek match the original results exactly.
*/