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
% Prove Goal1 implies Goal2: prove Goal2 if Goal1 is provable
prove(implies(Goal1, Goal2)) :-
    prove(Goal1),
    prove(Goal2).

% Prove the opposite of Goal: succeed if Goal is not provable
prove(opposite(Goal)) :-
    \+ prove(Goal).

% Expand Term into ExpandedTerm using defined rules
prove(expand(Term, ExpandedTerm)) :-
    expand(Term, ExpandedTerm).

% Prove that Elem is included in List
prove(includes(List, Elem)) :-
    member(Elem, List).

% Extend List by adding Elem to the head
prove(extend(List, Elem, [Elem|List])).

% Refute Goal: succeed if Goal is not provable
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

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is mostly correct and consistent with the original code. However, there is a significant difference in the implementation of the 'implies' predicate. The original code allows the implication to succeed if either the antecedent is unprovable or the consequent is provable, while the generated code requires both the antecedent and consequent to be provable. This change alters the logical meaning of 'implies'. Despite this, the running results are consistent for the given queries, as they happen to satisfy both implementations.
*/