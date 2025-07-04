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
prove(implies(Goal1, Goal2)) :-
    (prove(Goal1) -> prove(Goal2)).

prove(opposite(Goal)) :-
    \+ prove(Goal).

prove(expand(Term, Result)) :-
    expand(Term, Result).

prove(includes(List, Elem)) :-
    member(Elem, List).

prove(extend(List, Elem, [Elem|List])).

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
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 17:19. 

***Report:***
Validity_form:False\Validity_result:False
The generated code has a significant issue in the 'implies' predicate implementation. While the original code uses a disjunction (;), the generated code incorrectly uses a Prolog implication (->), which is not valid in ProbLog syntax. This causes the 'UnknownClause' error during execution. Other predicates are correctly implemented and match the original code's functionality. The generated code would be valid if not for this syntax error in the 'implies' predicate.