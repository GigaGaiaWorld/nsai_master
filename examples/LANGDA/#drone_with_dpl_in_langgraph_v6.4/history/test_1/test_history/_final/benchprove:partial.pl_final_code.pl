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
	
prove(implies(P,Q)) :-
    (\+ prove(P); prove(Q))
.
prove(opposite(P)) :-
	
prove(opposite(P)) :-
    \+ prove(P)
.
prove(expand(A,B)) :-
	expand(A,B).
prove(includes(Set,X)) :-
	member(X,Set).
prove(extend(List,Elem,Extended)) :-
	
prove(extend(List,Elem,Extended)) :-
    Extended = [Elem|List]
.
prove(refute(P)) :-
	\+ prove(P).
% --------- Examples ---------- %
% Define some expand rules:
expand(double(X), Y) :-
    Y is X*2
.
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
    rf = self.fold(
         ^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/parser.py", line 1101, in fold
    raise ParseError(
problog.parser.ParseError: Operator priority clash at 18:21. 

***Report:***
Validity_form:False\Validity_result:False
The generated code has several issues. First, there are duplicate definitions for `prove(implies(P,Q))` and `prove(opposite(P))`, which causes a syntax error. Second, the formatting is inconsistent, with some rules having unnecessary line breaks and spaces. These issues make the generated code invalid and unable to run, unlike the original code which runs successfully. The generated code does not meet the requirements due to these syntax errors.