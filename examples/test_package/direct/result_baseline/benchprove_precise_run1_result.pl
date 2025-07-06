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
% result1: true  % prove(implies(parent(alice,bob), ancestor(alice,bob))) succeeds because parent(alice,bob) is provable and ancestor(alice,bob) is provable
result2: true  % prove(opposite(parent(carol,alice))) succeeds because parent(carol,alice) is unprovable
result3: true  % prove(expand(double(3),6)) succeeds because 3*2=6
result4: true  % prove(includes([a,b,c],b)) succeeds because b is a member of [a,b,c]
result5: true  % prove(extend([1,2],3,[3,1,2])) succeeds because prepending 3 to [1,2] gives [3,1,2]

/* Result Report:
Validity_form: False
Validity_result: True
Report: The generated code is mostly correct and consistent with the original code. It includes definitions for the required predicates and correctly implements the meta-interpreter for proving goals. The generated code also includes the necessary examples and queries to match the original results. However, the generated code uses 'langda(LLM:...)' which is not standard Prolog or ProbLog syntax, and this might cause issues in actual execution. Despite this, the logic and expected results align with the original code.
*/