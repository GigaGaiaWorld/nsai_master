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
% 1. implies(P,Q): P ⇒ Q, when P is unprovable or Q is provable
prove(implies(P,Q)) :-
	( \+ prove(P) % if P is unprovable
	; prove(Q) ).
 % or Q is provable
% 2. opposite(P): "opposite"/negation of P; that is, P is unprovable
prove(opposite(P)) :-
	\+ prove(P).
% 3. expand(A,B): first use expand/2 rule to expand A into B, then prove B
% You need to define several expand/2 facts or rules in the program
prove(expand(A,B)) :-
	expand(A,B).
% 4. includes(Set,X): set inclusion relation, equivalent to member/2
prove(includes(Set,X)) :-
	member(X,Set).
% 5. extend(List,Elem,Extended): add Elem to the head of List to get Extended
prove(extend(List,Elem,Extended)) :-
	Extended = [Elem|List].
% 6. refute(P): refute, equivalent to "unprovable"
prove(refute(P)) :-
	\+ prove(P).
% --------- Examples ---------- %
% facts:
parent(alice, bob).
parent(bob, carol).
% Define some expand rules:
expand(parent(X,Y), ancestor(X,Y)) :- parent(X,Y).
expand(ancestor(X,Y), ancestor(X,Z)) :- parent(X,Z), ancestor(Z,Y).
query(prove(implies(parent(alice,bob), ancestor(alice,bob)))).

*** Result:*** 
Error evaluating Problog model:
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_builtin.py", line 257, in _builtin_clause
    clause_ids = database.get_node(clause_def).children
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'tuple' object has no attribute 'children'