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
% 1. implies/2: succeeds if the implication holds
prove(implies(A, B)) :-
    (prove(A) -> prove(B)).

% 2. opposite/1: succeeds if the negation holds
prove(opposite(A)) :-
    \+ prove(A).

% 3. expand/2: uses already defined rules
prove(expand(Goal, Result)) :-
    expand(Goal, Result).

% 4. includes/2: succeeds if the element is in the list
prove(includes(List, Elem)) :-
    member(Elem, List).

% 5. extend/2: adds Elem to the head of List
prove(extend(List, Elem, [Elem|List])).

% 6. refute/1: succeeds if the goal cannot be proven
prove(refute(A)) :-
    \+ prove(A).
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
problog.engine.UnknownClause: No clauses found for ''->'/2' at 18:15. 

***Report:***
Validity_form:False\Validity_result:False
The generated code is mostly consistent with the original code in terms of functionality and structure. However, there is a critical error in the 'implies/2' implementation where it uses '->/2' which is not recognized by ProbLog, leading to a runtime error. The original code correctly implements implication using ';' (or) and '\+' (not). Other parts of the generated code are valid and match the original code's functionality.