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

implies(A, B) :- prove(A), prove(B).
opposite(A) :- \+ prove(A).
expand(Goal, Result) :- clause(Goal, Body), prove(Body), Result = Goal.
includes(List, Elem) :- member(Elem, List).
extend(List, Elem, [Elem|List]).
refute(Goal) :- opposite(Goal).
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
    return [
           ^
  File "/Users/zhenzhili/MASTERTHESIS/#Expert_System_Design/langda/utils/test_tools.py", line 17, in timeout_handler
    raise TimeoutError(f"Function timed out while processing file: {file_basename}")
TimeoutError: Function timed out while processing file: benchprove:rough.pl_run3 

***Report:***
Validity_form:False\Validity_result:False
The generated code has several issues. First, it incorrectly defines 'implies(A, B)' as 'prove(A), prove(B)', which does not match the original's logic of 'P ⇒ Q' (P implies Q if P is unprovable or Q is provable). Second, the 'expand(Goal, Result)' definition is problematic as it reuses the 'expand' predicate name for both the rule and the meta-interpreter, causing potential conflicts. The original code clearly separates these. The generated code also lacks the proper handling of compound goals and the 'refute' predicate is redundantly defined as 'opposite'. These inconsistencies lead to a timeout error during execution, indicating the code is not functionally equivalent to the original.