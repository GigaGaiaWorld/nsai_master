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
	langda(LLM:"P ⇒ Q, when P is unprovable or Q is provable").

prove(opposite(P)) :-
	langda(LLM:"opposite/negation of P; that is, P is unprovable").

prove(expand(A,B)) :-
	langda(LLM:"use defined expand/2 rules below to expand A into B.").

prove(includes(Set,X)) :-
	langda(LLM:"set inclusion relation, equivalent to member/2").

prove(extend(List,Elem,Extended)) :-
	langda(LLM:"add Elem to the head of List to get Extended").

% 6. refute(P): refute, equivalent to "unprovable"
prove(refute(P)) :-
	\+ prove(P).

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
% result1: prove(implies(parent(alice,bob), ancestor(alice,bob))) :- true.
result2: prove(opposite(parent(carol,alice))) :- true.
result3: prove(expand(double(3),6)) :- true.
result4: prove(includes([a,b,c],b)) :- true.
result5: prove(extend([1,2],3,[3,1,2]))) :- true.

/* Result Report:
Validity_form: False
Validity_result: True
Report: The generated code is mostly correct and consistent with the original code. It includes definitions for the meta-interpreter and extended logic processing, as well as examples and queries that match the original results. However, there is a syntax error in the generated code (an extra closing parenthesis in result5). The running results are consistent with the original code, proving the same queries successfully.
*/