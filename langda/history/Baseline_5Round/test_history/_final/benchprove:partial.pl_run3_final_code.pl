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
    \+ prove(P); prove(Q).

prove(opposite(P)) :-
    \+ prove(P).

prove(expand(A,B)) :-
    expand(A,B).

prove(includes(Set,X)) :-
    member(X,Set).

prove(extend(List,Elem,Extended)) :-
    Extended = [Elem|List].

prove(refute(P)) :-
    \+ prove(P).

% --------- Examples ---------- %
% Define some expand rules:
expand(X,Y) :- Y is X*2.

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
    cleanup, actions = node()  # Evaluate the node
                       ^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/eval_nodes.py", line 872, in __call__
    raise ArithmeticError(base_message, location)
problog.logic.ArithmeticError: Error while evaluating 'is'(6,double(3)*2): Unknown function 'double'/1 at 40:18. 

***Report:***
Validity_form:False\Validity_result:False
The generated code is mostly consistent with the original code but has a critical issue in the 'expand' rule definition. The original code defines specific expand rules like 'double(X)' and 'square(X)', whereas the generated code incorrectly defines a generic 'expand(X,Y)' rule, leading to an evaluation error. This makes the generated code invalid for the intended queries, particularly for 'prove(expand(double(3),6))'. The running results are inconsistent due to this error.