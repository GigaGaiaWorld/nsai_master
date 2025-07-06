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
langda(LLM:"Extended define multiple prove/1 logic processing predicates, which should contain:
	1.implies/2
	2.opposite/1
	3.expand/2 (use already defined rules)
	4.includes/2
	5.extend/2(add Elem to the head of List)
	6.refute/1").

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

% Predicted results by DeepSeek:
% result1: prove(implies(parent(alice,bob), ancestor(alice,bob))) :- true
result2: prove(opposite(parent(carol,alice))) :- true
result3: prove(expand(double(3),6)) :- true
result4: prove(includes([a,b,c],b)) :- true
result5: prove(extend([1,2],3,[3,1,2])) :- true

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code is mostly correct and consistent with the original code. It includes the required predicates (implies/2, opposite/1, expand/2, includes/2, extend/2) and the meta-interpreter for prove/1. However, the generated code lacks the actual definitions for some predicates like implies/2, opposite/1, includes/2, and extend/2, which are necessary for the queries to succeed as shown in the original results. The running results in the generated code are marked as 'true' by DeepSeek's prediction, but without the actual predicate definitions, these results cannot be verified programmatically.
*/