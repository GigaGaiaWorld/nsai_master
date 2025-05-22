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
prove(implies(A, B)) :- (prove(A), prove(B)); \+ prove(A).
prove(opposite(A)) :- \+ prove(A).
prove(expand(Goal, Result)) :- call(Goal, Result).
prove(includes(List, Elem)) :- member(Elem, List).
prove(extend(List, Elem, [Elem|List])).
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

*** Result:*** 
Error evaluating Problog model:
    actions = engine.call_intern(
              ^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 573, in call_intern
    raise UnknownClause(query.signature, database.lineno(query.location))
problog.engine.UnknownClause: No clauses found for 'double/2' at 33:20. 

***Report:***
Validity_form:False\Validity_result:False
The generated code has several issues. First, the 'prove(expand(Goal, Result))' clause incorrectly uses 'call(Goal, Result)' instead of 'expand(Goal, Result)', leading to an error when evaluating 'double/2'. Second, the 'prove(extend(List, Elem, [Elem|List]))' clause is missing the body, which should verify the equality. The generated code is not consistent with the original code in these aspects, causing it to fail during execution.