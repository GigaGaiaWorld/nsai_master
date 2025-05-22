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
% implies/2: P implies Q
prove(implies(P, Q)) :-
    (prove(P), prove(Q)) ; (\+ prove(P)).

% opposite/1: Negation of a goal
prove(opposite(Goal)) :-
    \+ prove(Goal).

% expand/2: Use already defined rules to expand a term
prove(expand(Term, Result)) :-
    expand(Term, Result).

% includes/2: Check if an element is in a list
prove(includes(List, Elem)) :-
    member(Elem, List).

% extend/2: Add Elem to the head of List
prove(extend(List, Elem, [Elem|List])).

% refute/1: Prove the negation of a goal
prove(refute(Goal)) :-
    \+ prove(Goal).
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
The generated code is largely correct and consistent with the original code. It maintains the same functionality for member/2, the basic meta-interpreter, and extended logic processing. The generated code simplifies the 'implies' definition slightly but maintains equivalent semantics. All other extended logic predicates (opposite, expand, includes, extend, refute) are correctly replicated. The examples and queries are identical to the original, ensuring the same behavior. The running results are completely consistent between both versions.