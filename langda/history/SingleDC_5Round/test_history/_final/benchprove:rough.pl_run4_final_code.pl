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
    (prove(Goal1) -> prove(Goal2).

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
    return self.collapse(string, tokens)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/parser.py", line 1282, in collapse
    raise UnmatchedCharacter(string, expr_stack[-1].start.location)
problog.parser.UnmatchedCharacter: Unmatched character '(' at 17:5. 

***Report:***
Validity_form:False\Validity_result:False
The generated code has a syntax error in the 'implies' predicate, missing a closing parenthesis and the 'else' part of the conditional statement. This makes the code invalid and unable to run. The original code correctly implements the 'implies' predicate using a disjunction (;), while the generated version incorrectly uses a conditional (->) without proper syntax. Other predicates are correctly replicated from the original code, but the syntax error prevents the code from being valid.